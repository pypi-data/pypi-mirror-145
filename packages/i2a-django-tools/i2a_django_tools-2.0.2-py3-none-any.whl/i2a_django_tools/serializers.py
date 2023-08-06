from django.core.exceptions import ObjectDoesNotExist
from django.utils.duration import duration_iso_string
from rest_framework import serializers
from django.db.models import DurationField
from rest_framework.fields import DecimalField, Field
from enumfields.drf import EnumField, EnumSupportSerializerMixin
from timezone_field import TimeZoneField

import fields


class BaseModelSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    pass


class FilteredByPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Just like PrimaryKeyRelatedField, but also filters the queryset by account_id
    taken from request. Other values to filter by might be specified by using
    `extra_dynamic_lookup_fields`, but they need to correspond to variables
    on the request object.

    fail_silently: when True, objects that don't exist in the db are returned as None
    """

    def __init__(
        self,
        lookup_field="pk",
        repr_field="pk",
        extra_dynamic_lookup_fields: dict = None,
        fail_silently=False,
        distinct=False,
        *args,
        **kwargs,
    ):
        self.lookup_field = lookup_field
        self.extra_dynamic_lookup_fields = extra_dynamic_lookup_fields
        self.repr_field = repr_field
        self.fail_silently = fail_silently
        self.distinct = distinct
        if self.lookup_field != "pk":
            self.default_error_messages[
                "does_not_exist"
            ] = f"Invalid {self.lookup_field} {{pk_value}} - object does not exist."
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        request = self.context.get("request", None)
        queryset = super().get_queryset()
        if not request:
            return queryset.none()
        dynamic_lookup = {}
        if self.extra_dynamic_lookup_fields:
            for path, value in self.extra_dynamic_lookup_fields.items():
                assert hasattr(request, value)
                dynamic_lookup[path] = getattr(request, value)
        qs = queryset.filter(**dynamic_lookup)
        if self.distinct:
            qs = qs.distinct()
        return qs

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return self.get_queryset().get(**{self.lookup_field: data})
        except ObjectDoesNotExist:
            if not self.fail_silently:
                self.fail("does_not_exist", pk_value=data)
            return None
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)

    def use_pk_only_optimization(self):
        if self.repr_field == "pk":
            return True
        return False

    def to_representation(self, value):
        field = getattr(value, self.repr_field)
        if self.pk_field is not None:
            return self.pk_field.to_representation(field)
        return field


class AmountField(DecimalField):

    def __init__(
        self, *, max_digits=12, decimal_places=2, min_value=0, **kwargs
    ):
        super().__init__(
            decimal_places=decimal_places, max_digits=max_digits,
            min_value=min_value,
            **kwargs
        )


class PercentField(DecimalField):

    def __init__(
        self, *, max_digits=12, decimal_places=2, min_value=0, max_value=1,
        **kwargs
    ):
        super().__init__(
            decimal_places=decimal_places, max_digits=max_digits,
            min_value=min_value, max_value=max_value,
            **kwargs
        )


class IntEnumToStringField(Field):

    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return self.enum(value).label


class ISODurationField(DurationField):

    def to_representation(self, value):
        return duration_iso_string(value)


class EnhancedModelSerializer(BaseModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        **{
            fields.AmountField: AmountField,
            fields.PercentField: PercentField,
            TimeZoneField: serializers.CharField,
            DurationField: ISODurationField,
        }
    }
