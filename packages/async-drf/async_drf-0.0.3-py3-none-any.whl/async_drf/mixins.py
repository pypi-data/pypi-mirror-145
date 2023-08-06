import asyncio as aio
import typing

from asgiref.sync import sync_to_async
from rest_framework import status, mixins
from rest_framework.response import Response


class AsyncMixin:
    """Provides async view compatible support for DRF Views and ViewSets.

    This must be the first inherited class.

        class MyViewSet(AsyncMixin, GenericViewSet):
            pass
    """

    @classmethod
    def as_view(cls, *args, **initkwargs):
        """Make Django process the view as an async view.
        """
        view = super().as_view(*args, **initkwargs)

        async def async_view(*args, **kwargs) -> typing.Callable[[typing.Any], Response]:
            # wait for the `dispatch` method
            return await view(*args, **kwargs)

        async_view.csrf_exempt = True
        return async_view

    async def dispatch(self, request, *args, **kwargs):
        """Add async support.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            await sync_to_async(self.initial)(request, *args, **kwargs)  # MODIFIED HERE

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # accept both async and sync handlers
            # built-in handlers are sync handlers
            if not aio.iscoroutinefunction(handler):  # MODIFIED HERE
                handler = sync_to_async(handler)  # MODIFIED HERE
            response = await handler(request, *args, **kwargs)  # MODIFIED HERE

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class AsyncCreateModelMixin(mixins.CreateModelMixin):
    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)  # MODIFIED HERE
        await self.perform_create(serializer)  # MODIFIED HERE
        serializer_data = await sync_to_async(getattr)(serializer, 'data')
        headers = self.get_success_headers(serializer_data)
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)

    async def perform_create(self, serializer):
        await sync_to_async(serializer.save)()


class AsyncListModelMixin:
    async def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = await sync_to_async(self.paginate_queryset)(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = await sync_to_async(getattr)(serializer, 'data')
            return await sync_to_async(self.get_paginated_response)(serializer_data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_data = await sync_to_async(getattr)(serializer, 'data')
        return Response(serializer_data)


class AsyncRetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    async def retrieve(self, request, *args, **kwargs):
        instance = await self.get_object()
        serializer = self.get_serializer(instance)
        serializer_data = await sync_to_async(getattr)(serializer, 'data')
        return Response(serializer_data)


class AsyncUpdateModelMixin:
    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = await self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        await self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer_data = await sync_to_async(getattr)(serializer, 'data')
        return Response(serializer_data)

    async def perform_update(self, serializer):
        await sync_to_async(serializer.save)()

    async def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return await self.update(request, *args, **kwargs)


class AsyncDestroyModelMixin:
    async def destroy(self, request, *args, **kwargs):
        instance = await self.get_object()  # MODIFIED HERE
        await self.perform_destroy(instance)  # MODIFIED HERE
        return Response(status=status.HTTP_204_NO_CONTENT)

    async def perform_destroy(self, instance):
        await sync_to_async(instance.delete)()  # MODIFIED HERE
