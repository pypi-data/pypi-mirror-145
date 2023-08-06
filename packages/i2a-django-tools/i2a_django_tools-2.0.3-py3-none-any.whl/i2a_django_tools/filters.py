from collections import defaultdict
from functools import reduce

from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django_filters import NumberFilter, CharFilter, BaseInFilter, BooleanFilter
from rest_framework.exceptions import ValidationError
from rest_framework_filters import filters, FilterSet, RelatedFilter
from rest_framework_filters.filterset import related

from i2a_django_tools.models import LIVE_REVISION_ID


class FilterUtils:

    @staticmethod
    def get_filters(class_filter, request_filters, key_prefix=''):
        for key, filter_instance in class_filter.base_filters.items():
            key = key_prefix + key
            if filter_instance.__class__ is RelatedFilter:
                request_filters += FilterUtils.get_filters(
                    filter_instance.filterset, [], key_prefix=key + '__'
                )
            request_filters.append(key)
        return request_filters

    @staticmethod
    def generate_filters_for_calculated_fields(calculated_fields, vars_cls):
        for field_name, field_lookups in calculated_fields.items():
            for field_lookup in field_lookups:
                if field_lookup == 'exact':
                    vars_cls[field_name] = NumberFilter(lookup_expr=field_lookup,
                                                        field_name=field_name)
                elif field_lookup == 'in':
                    vars_cls[field_name] = NumberFilter(lookup_expr=field_lookup,
                                                        field_name=field_name)
                elif field_lookup == 'range':
                    vars_cls[field_name] = NumberFilter(lookup_expr=field_lookup,
                                                        field_name=field_name)
                else:
                    vars_cls[field_name + '__' + field_lookup] = NumberFilter(
                        lookup_expr=field_lookup,
                        field_name=field_name)


class CustomFilterSet(FilterSet):
    """
    Custom filter class to extend functionalities.
        IMPORTANT - It has to be the first serializer in the inherence hierarhy.
    FEATURES:
       !!= query filter operator. Adding for every model sub patch an condition to include nullable ids.
       example:
        (a) ?model_X__model_Y__model_Z__id__in!=1,2,3 vs (b) ?model_X__model_Y__model_Z__id__in!!=1,2,3
       (a) SQL:
           WHERE Z.ID in (1,2,3)  |NOTE: it excludes records which do not have relation to Z!
       (b) SQL:
           WHERE Z.ID in (1,2,3)
           OR X.ID is NULL
           OR Y.ID is NULL
           OR Z.ID is NULL
    """
    def __init__(self, data=None, *args, is_nested_filter_set=False, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.is_nested_filter_set = is_nested_filter_set
        self.query_paths = defaultdict(set)
        self.nested_query_filter_set_with_double_negations_dict = {}

        data = self._prepare_custom_filter_data(data)
        super().__init__(data, *args, **kwargs)

    def filter_related_filtersets(self, queryset):
        """
            Overwritten method from FilterSet class.
            for our operator !!= we produce separate condition set with prover flat null=false flags.
            Normally filter produce subquery trees but what we do is dividing them into subquery paths which
            proper is_null filters and connect them with ands. This is UBER Tricky.
        """
        for related_name, related_filterset in self.related_filtersets.items():
            prefix = '%s%s' % (related(self, related_name), LOOKUP_SEP)
            if not any(value.startswith(prefix) for value in self.data):
                continue

            field = self.filters[related_name].field
            to_field_name = getattr(field, 'to_field_name', 'pk') or 'pk'

            field_name = self.filters[related_name].field_name
            lookup_expr = LOOKUP_SEP.join([field_name, 'in'])
            subquery = related_filterset.qs.values(to_field_name)
        # CUSTOM CODE | Added it to add extra conditions, works only on the main PARENT in the relation tree
            # query path exists only is the nested filter set is True.
            if field_name in self.query_paths and self.is_nested_filter_set:
                conditions = [Q(**{f'{field_path}__isnull': True}) for field_path in self.query_paths[field_name]]
                queryset = queryset.filter(reduce(lambda x, y: x | y, conditions) | Q(**{lookup_expr: subquery}))
            else:
                queryset = queryset.filter(**{lookup_expr: subquery})
            # handle distinct
            if self.related_filters[related_name].distinct:
                queryset = queryset.distinct()
        if not self.is_nested_filter_set:
            for name, value in self.nested_query_filter_set_with_double_negations_dict.items():
                data = {name: value}
                filter_set = self.__class__(data, *self.args, is_nested_filter_set=True, **self.kwargs)
                filter_set.is_valid()
                queryset = filter_set.filter_queryset(queryset)
        # END OF CUSTOM CODE
        return queryset

    def _prepare_custom_filter_data(self, data):
        """
        This is additional method added by us.
        Aim: This method has two reasons.
            1. Overwrite data to replace double !! with single !.
            2. Prepare the filter paths to filter trough queryset once
               (we want to do so flat because of performance issues)
        """
        modified_data = {}

        for name, value in data.items():
            if name.endswith('!!'):
                # TODO: Add validate filters.
                if self.is_nested_filter_set:
                    if LOOKUP_SEP in name:
                        fields = name.split(LOOKUP_SEP)
                        key = fields[0]
                        path = key
                        current_serializer = self.related_filters[key]
                        if self.check_is_last_field_nullable(path):
                            self.query_paths[key].add(path)
                        #
                        for field in fields[1:]:
                            if field in current_serializer.filterset.related_filters:
                                path += f'__{field}'
                                current_serializer = current_serializer.filterset.related_filters[field]
                            else:
                                break
                            if self.check_is_last_field_nullable(path):
                                self.query_paths[key].add(path)
                    modified_data[name[:-1]] = value
                self.nested_query_filter_set_with_double_negations_dict[name] = value
            else:
                modified_data[name] = value
        return modified_data

    def check_is_last_field_nullable(self, path) -> bool:
        assert path
        current_field = None
        current_model = self.Meta.model
        nullable = False
        for field_name in path.split('__'):
            current_field = getattr(current_model, field_name).field
            if current_field.related_model != current_model:
                if current_field.many_to_many:
                    nullable = True
                else:
                    nullable = current_field.null
                current_model = current_field.related_model
            else:
                # Means that we are dealing with foreign key.
                current_model = current_field.model
                nullable = True
        assert current_field
        return nullable


class EnumIntegerFilter(NumberFilter):

    def __init__(self):
        super().__init__(method='filter_value')


class EnumIntegerFilterIn(CharFilter):

    def __init__(self):
        super().__init__(method='filter_value__in')


class IntegerInFilter(BaseInFilter, NumberFilter):
    pass


class EnumIntegerFilterMixin:

    @staticmethod
    def filter_value(queryset, name, value):
        if value:
            kwargs = {f'{name}__in': (value, )}
            return queryset.filter(Q(**kwargs))
        return queryset

    @staticmethod
    def filter_value__in(queryset, name, value):
        if value:
            values = value.split(',')
            values = [int(i) for i in values]
            kwargs = {f'{name}': values}
            return queryset.filter(Q(**kwargs))
        return queryset


class ArchiveFilterMixin(CustomFilterSet):

    is_archive = filters.BooleanFilter(method='filter_is_archive')

    @staticmethod
    def filter_is_archive(queryset, name, value):
        if value:
            return queryset.filter(archive_revision_id__lt=LIVE_REVISION_ID)
        else:
            return queryset.filter(archive_revision_id=LIVE_REVISION_ID)


class ValidateFilterSet(CustomFilterSet):

    def is_valid(self):
        available_filters = FilterUtils.get_filters(self.__class__, [])
        for key, _ in self.data.items():
            key_to_check = key.replace('!', '')
            if key_to_check in ('ordering', 'page_size', 'page'):
                continue
            if key_to_check not in available_filters:
                raise ValidationError(detail=[key])
        return super().is_valid()


class DeepMixedSearchFilterSet(CustomFilterSet):
    deep_mixed_search_fields: NotImplemented
    deep_mixed_search = filters.CharFilter(method='filter_deep_mixed_search')

    def filter_deep_mixed_search(self, queryset, field, value):
        if value:
            field = field.replace('deep_mixed_search', '')
            field_list = []
            for search_field in self.deep_mixed_search_fields:
                field_list.append(field + search_field)
            return queryset.annotate(
                search=SearchVector(*field_list)
            ).filter(
                Q(search__icontains=value) |
                Q(search=value)
            )
        return queryset


class ArchiveFilterSet(CustomFilterSet):
    is_archived = BooleanFilter(
        method='filter_is_archived'
    )

    @staticmethod
    def filter_is_archived(queryset, name, value):
        if value is True:
            return queryset.archived()
        elif value is False:
            return queryset.published()
        return queryset

