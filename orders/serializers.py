from rest_framework import serializers
from .models import Order, OrderItem
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_slug', 'quantity', 'price', 'product_image', 'subtotal']

    @extend_schema_field(OpenApiTypes.URI)
    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.product.images.first()
        return primary_image.image.url if primary_image else None

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_subtotal(self, obj):
        return obj.subtotal

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'order_id', 'subtotal', 'total', 'created_at']
