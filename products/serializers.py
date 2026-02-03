from datetime import timezone
from .models import Product, ProductImage, Category, Tag, Brand, Review
from users.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.utils.timesince import timesince
from django.utils import timezone


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
    children = serializers.SerializerMethodField()  # Recursive for tree structure

    @extend_schema_field(OpenApiTypes.INT)
    def get_product_count(self, obj):
        # Recursive count including subcategories (efficient with MPTT)
        descendants = obj.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants).count()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_children(self, obj):
        if obj.is_leaf_node():
            return []
        return CategorySerializer(obj.get_children(), many=True).data

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count', 'children']


class CategoryLeafSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_product_count(self, obj):
        # For leaves, just count direct products (no descendants needed)
        return Product.objects.filter(category=obj).count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']


