### Django REST framework async views


## How to use
```
from async_drf.mixins import AsyncMixin, AsyncListModelMixin
from async_drf.viewsets import AsyncGenericViewSet

class ProductsViewSet(AsyncMixin, AsyncGenericViewSet, AsyncListModelMixin):
	serializer_class = ProductsSerializer
	queryset = ProductModel.objects.prefetch_related().all()

	async def list(self, request: Request, *args, **kwargs):
	    # do async stuff here
		return Response(data=data)
```

