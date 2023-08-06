from django.core import validators
from django.db import models
from django.utils.functional import cached_property


class AmountField(models.DecimalField):

    def __init__(self, *, max_digits=12, decimal_places=2, **kwargs):
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, **kwargs
        )

    @cached_property
    def validators(self):
        return super().validators + [
            validators.MinValueValidator(0)
        ]


class PercentField(models.DecimalField):

    def __init__(self, *, max_digits=12, decimal_places=2, **kwargs):
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, **kwargs
        )

    @cached_property
    def validators(self):
        return super().validators + [
            validators.MinValueValidator(0),
            validators.MaxValueValidator(1),
        ]
