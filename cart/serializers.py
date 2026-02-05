from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ImageSerializer  # Reuse from products
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    price = serializers.DecimalField(source='product.current_price', read_only=True, max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    product_image = serializers.SerializerMethodField()

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
    class Meta:
        model = CartItem
        fields = ["id", "quantity"]

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")

        if quantity > self.instance.product.stock_count:
            raise serializers.ValidationError("Not enough stock available.")
        
        return quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.subtotal for item in obj.items.all())

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']