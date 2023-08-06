from asgiref.sync import sync_to_async
from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin

from .mixins import AsyncMixin, AsyncListModelMixin, AsyncRetrieveModelMixin, AsyncCreateModelMixin, AsyncUpdateModelMixin, AsyncDestroyModelMixin


class AsyncGenericViewSet(ViewSetMixin, generics.GenericAPIView):
	async def get_object(self):
		return await sync_to_async(super().get_object)()


class AsyncModelViewSet(AsyncMixin,
						AsyncListModelMixin,
						AsyncRetrieveModelMixin,
						AsyncCreateModelMixin,
						AsyncUpdateModelMixin,
						AsyncDestroyModelMixin,
						AsyncGenericViewSet):
	pass
