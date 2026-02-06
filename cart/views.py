from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemUpdateSerializer
from products.models import Product
from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve current user's cart", 
        tags=['Cart']), 
        responses={
            200: OpenApiResponse(
                response=CartSerializer(many=False),
                description="Cart retrieved successfully"
            ),
            401: OpenApiResponse(description="Unauthorized")
        }
)
class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


    @extend_schema(
        summary="Add item to cart",
        request=CartItemSerializer,
        responses={
            201: OpenApiResponse(description="Item added to cart"), 
            400: OpenApiResponse(description="Invalid data or insufficient stock"),
        },
        tags=['Cart']
    )
    @action(detail=False, methods=['post'], url_path='add')
    def add_item(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        if product.stock_count < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart = request.user.cart
        with transaction.atomic():
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                new_quantity = item.quantity + quantity
                if new_quantity > product.stock_count:
                    return Response({"error": f"Total quantity ({new_quantity}) exceeds available stock ({product.stock_count}) for {product.name}"},status=status.HTTP_400_BAD_REQUEST)
                
                item.quantity = new_quantity
            else:
                item.quantity = quantity

            item.save()

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update cart item quantity (send 'id' and 'quantity' in request body)",
        description="Requires JSON body with 'id' (item ID) and 'quantity' (new value).",
        request=CartItemUpdateSerializer,
        responses={
            200: CartItemUpdateSerializer,
            400: OpenApiResponse(description="Invalid quantity or insufficient stock"),
            404: OpenApiResponse(description="Item not found"),
        },
        tags=['Cart']
    )
    @action(detail=False, methods=['patch'], url_path='update')
    def update_item(self, request):
        item_id = request.data.get('id')
        if not item_id:
            return Response({'error': 'id required'}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)

        serializer = CartItemUpdateSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            if quantity > item.product.stock_count:
                return Response({'error': f"Not enough stock available for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="Remove item from cart",
        parameters=[
            OpenApiParameter(name='item_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, description='Item ID to remove', required=True),
        ],
        responses={
            204: OpenApiResponse(description="Item removed"),
            404: OpenApiResponse(description="Item not found"),
        },
        tags=['Cart']
    )
    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_item(self, request):
        item_id = request.query_params.get('item_id')
        item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @extend_schema(
        summary="Clear entire cart",
        responses={
            204: OpenApiResponse(description="Cart cleared"),
        },
        tags=['Cart']
    )
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        cart = request.user.cart
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 