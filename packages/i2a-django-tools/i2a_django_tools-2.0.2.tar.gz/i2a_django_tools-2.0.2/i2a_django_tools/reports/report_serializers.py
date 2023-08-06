from collections import OrderedDict
import pytz

from rest_framework.fields import SkipField, DateTimeField, DateField
from rest_framework.relations import PKOnlyObject

from django.conf import settings

from rest_framework import serializers


class BaseReportSerializer(serializers.Serializer):

    def __init__(
            self, *args, custom_timezone=pytz.timezone(settings.TIME_ZONE), datetime_format=None,
            date_format=None,
            **kwargs
    ):
        # In the endpoints, when they do not provide timezone, we use default UTC,
        # so the pattern UTC only API is not broken.
        super().__init__(*args, **kwargs)
        # New code
        self.custom_timezone = custom_timezone
        self.datetime_format = datetime_format
        self.date_format = date_format

    def __new__(cls, *args, **kwargs):
        """
            The whole method is copied from Serializer class,
             which cause using this class instead of ListSerializer to create children.
        """
        # We override this method in order to automagically create
        # `ListSerializer` classes instead when `many=True` is set.
        if kwargs.pop('many', False):
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def to_representation(self, instance):
        """
          Copied from serializer Class
          Added special method invocation for field that is instance of custom date time field
          Used for serializing data with special timezone in report.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                # New code
                if isinstance(field, DateTimeField):
                    field.timezone = self.custom_timezone
                    if self.datetime_format:
                        field.format = self.datetime_format
                if isinstance(field, DateField):
                    if self.date_format:
                        field.format = self.date_format
                # End of new code
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    def get_fields(self):
        """
        Returns a dictionary of {field_name: field_instance}.
        """
        fields = super().get_fields()
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'fields'):
            new_fields = OrderedDict()
            for key in self.Meta.fields:
                if key in fields:
                    new_fields[key] = fields[key]
                else:
                    raise Exception(
                        f"{key} is not in declared_fields for {self.__class__}"
                    )
            return new_fields
        return fields

    class Meta:
        summary_fields = []
        fields = []
