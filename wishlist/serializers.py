from rest_framework import serializers
from .models import Wishlist, WishlistItem
from products.serializers import ImageSerializer
from products.models import Product
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class WishlistItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    price = serializers.DecimalField(source='product.current_price', read_only=True, max_digits=10, decimal_places=2)
    stock_status = serializers.CharField(source='product.stock_status', read_only=True)
    product_image = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_product_image(self, obj):
        primary = obj.product.images.filter(is_primary=True).first()
        if primary:
            return ImageSerializer(primary).data
        return None

    class Meta:
        model = WishlistItem
        fields = ['id', 'product_id', 'product_name', 'product_slug', 'product_image', 'price', 'stock_status']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'items']