from rest_framework import serializers
from .models import Product, ProductImage, Category
from drf_spectacular.utils import extend_schema_field
from typing import Optional, Dict, Any, List
from drf_spectacular.types import OpenApiTypes


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url', allow_null=True, default=None)

    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary']

class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()  # Only primary image
    stock_status = serializers.CharField(read_only=True) 

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_images(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return ImageSerializer(primary).data
        return None

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'current_price', 'original_price', 'discount_percentage', 'average_rating', 'stock_status', 'images']

class ProductDetailSerializer(serializers.ModelSerializer):
    stock_status = serializers.CharField(read_only=True) 
    category = serializers.CharField(source='category.name', read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    additional_info = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_additional_info(self, obj):
        return {
            'weight': obj.weight,
            'color': obj.color,
            'type': obj.type,
            'stock_count': obj.stock_count,
            'tags': [tag.name for tag in obj.tags.all()]
        }

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'sku', 'current_price', 'original_price', 'discount_percentage', 'average_rating', 'reviews_count', 'stock_status', 'category', 'description', 'additional_info', 'images']

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_product_count(self, obj):
        # Recursive count including subcategories (efficient with MPTT)
        descendants = obj.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants).count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']

