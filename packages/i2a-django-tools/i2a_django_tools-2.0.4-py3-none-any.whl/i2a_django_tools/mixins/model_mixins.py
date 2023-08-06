from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class SameOutputCreateModelMixin:

    def create(self: GenericViewSet, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_serializer = self.serializer_class(
                instance=self.get_queryset().get(id=serializer.instance.id)
            )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def perform_create(serializer):
        serializer.save()


class CustomUpdateModelMixin:

    """
    Update a model instance (without Partial Update).
    """

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @staticmethod
    def perform_update(serializer):
        serializer.save()


class PartialUpdateModelMixin:

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @staticmethod
    def perform_update(serializer):
        serializer.save()
