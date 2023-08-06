from django.core.paginator import Paginator as DjangoPaginator
from django.db.models.expressions import Col
from django.db.models.sql.where import NothingNode, WhereNode
from django.utils.functional import cached_property


class CustomDjangoPaginator(DjangoPaginator):

    def _check_children(self, children) -> bool:
        return all(
            [
               self._check_child(child) for child in children
             ]
        )

    def _check_child(self, child) -> bool:
        """return True if query can be optimized"""
        if not isinstance(child, NothingNode):
            if isinstance(child, WhereNode):
                return self._check_children(child.children)
            else:
                if not isinstance(child.lhs, Col):
                    return False
        return True

    @staticmethod
    def _check_ordering(query) -> bool:
        """return True if query can be optimized"""
        return not any(
            order_by.replace('-', '') in query.annotations for order_by in query.order_by
        )

    def _can_optimize(self, query) -> bool:
        """return True if query can be optimized"""
        if self._check_children(query.where.children) and self._check_ordering(query):
            return True
        return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pre_filtered_queryset = None
        self.can_optimize = self._can_optimize(self.object_list.query)
        if self.can_optimize:
            normal_queryset = self.object_list.query.model.objects.all()
            self.pre_filtered_queryset = self.object_list.all()
            self.pre_filtered_queryset.query.annotation_select.clear()
            self.pre_filtered_queryset.query.annotation_select.update(normal_queryset.query.annotation_select)

            self.pre_filtered_queryset.query.annotations.clear()
            self.pre_filtered_queryset.query.annotations.update(normal_queryset.query.annotations)

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count

        # Our injection
        if self.can_optimize:
            self.object_list = self.object_list.filter(
                    id__in=list(
                        self.pre_filtered_queryset[bottom:top].values_list('id', flat=True)
                    )
                )
            return self._get_page(self.object_list, number, self)
        # End of our injection
        return self._get_page(self.object_list[bottom:top], number, self)

    @cached_property
    def count(self):
        """
        Returns the total number of objects, across all pages.
        """
        if self.can_optimize:
            queryset = self.pre_filtered_queryset
        else:
            queryset = self.object_list
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)
