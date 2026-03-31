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
    category = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_images(self, obj):
        for img in obj.images.all():  # uses prefetch cache, zero extra queries
            if img.is_primary:
                return ImageSerializer(img).data
        return None
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_category(self, obj):
        return obj.category.name if obj.category else None

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'current_price', 'original_price', 'discount_percentage', 'average_rating', 'stock_status', 'category', 'images']

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


class CategoryRootSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_product_count(self, obj):
        # Count products in this category + ALL subcategories
        descendants = obj.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants).count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url', allow_null=True, default=None)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'image']


class UserReviewSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    image = serializers.CharField(source='profile.image.url', allow_null=True, default=None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.email

    @extend_schema_field(OpenApiTypes.STR)
    def get_email(self, obj):
        return  obj.email

    class Meta:
        model = User
        fields = ['full_name', 'email', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_created_at(self, obj):
        now = timezone.now()
        delta = now - obj.created_at
        if delta.days == 0:
            return timesince(obj.created_at) + ' ago'
        elif delta.days < 8:
            return f"{delta.days} days ago"
        else:
            return obj.created_at.strftime('%Y-%m-%d')

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # user and product are set in view
        extra_kwargs = {
            'rating': {'required': True},
        }
