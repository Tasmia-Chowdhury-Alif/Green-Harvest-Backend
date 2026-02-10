from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ImageSerializer  # Reuse from products
from products.models import Product
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    price = serializers.DecimalField(source='product.current_price', read_only=True, max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    product_image = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_product_image(self, obj):
        primary = obj.product.images.filter(is_primary=True).first()
        if primary:
            return ImageSerializer(primary).data
        return None

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'product_slug', 'product_image', 'price', 'quantity', 'subtotal']


class CartItemUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating cart item quantity."""
    id = serializers.IntegerField(help_text="The ID of the cart item to update", required=True)
    quantity = serializers.IntegerField(min_value=0, help_text="New quantity for the cart item", required=True)

    class Meta:
        model = CartItem
        fields = ["id", "quantity"]

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total_price(self, obj):
        return obj.total

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']