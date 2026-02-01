from rest_framework import serializers
from .models import Product, ProductImage, Category

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url')  # Cloudinary gives URL

    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary']

class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()  # Only primary image
    stock_status = serializers.ReadOnlyField()

    def get_images(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return ImageSerializer(primary).data
        return None

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'current_price', 'original_price', 'discount_percentage', 'average_rating', 'stock_status', 'images']

class ProductDetailSerializer(serializers.ModelSerializer):
    stock_status = serializers.ReadOnlyField()
    category = serializers.CharField(source='category.name', read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    additional_info = serializers.SerializerMethodField()

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

    def get_product_count(self, obj):
        # Recursive count including subcategories (efficient with MPTT)
        descendants = obj.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants).count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']