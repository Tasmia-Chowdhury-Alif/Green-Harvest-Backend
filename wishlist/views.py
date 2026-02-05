from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, WishlistItemSerializer
from products.models import Product
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve current user's wishlist", 
        tags=['Wishlist']),
        responses={200: WishlistSerializer(many=False)}
)
class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wishlist)
        return Response(serializer.data)

    @extend_schema(
        summary="Add item to wishlist",
        request=WishlistItemSerializer,
        responses={201: OpenApiResponse(description="Item added to Wishlist"), 400: OpenApiResponse(description="Item already in wishlist"),},
        tags=['Wishlist']
    )
    @action(detail=False, methods=['post'], url_path='add')
    def add_item(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        wishlist = request.user.wishlist
        item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        if not created:
            return Response({'error': 'Item already in wishlist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WishlistItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Remove item from wishlist",
        parameters=[
            OpenApiParameter(name='item_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, description='Item ID to remove', required=True),
        ],
        responses={204: OpenApiResponse(description="Item removed")},
        tags=['Wishlist']
    )
    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_item(self, request):
        item_id = request.query_params.get('item_id')
        item = get_object_or_404(WishlistItem, id=item_id, wishlist=request.user.wishlist)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Clear entire wishlist",
        responses={
            204: OpenApiResponse(description="Wishlist cleared"),
        },
        tags=['Wishlist']
    )
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_wishlist(self, request):
        wishlist = request.user.wishlist
        wishlist.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

