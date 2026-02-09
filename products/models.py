from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from decimal import Decimal

# Choices for stock status
class StockStatus(models.TextChoices):
    IN_STOCK = 'IN_STOCK', 'In Stock'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'

class Category(MPTTModel):
    """Hierarchical category model using MPTT."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Tag(models.Model):
    """Tag model for products."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Brand(models.Model):
    """Product brand model."""
    name = models.CharField(max_length=100, unique=True)
    image = CloudinaryField('image', folder='greenharvest_images/brands', null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    """Product model for product items."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))]) 
    average_rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    weight = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=100, blank=True)
    stock_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=['slug', 'category', 'brand'])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-gen SKU if blank (simple UUID-based)
        if not self.sku:
            self.sku = f"GH-{uuid.uuid4().hex[:8].upper()}"
        # Compute current_price (simple save-based)
        if self.discount_percentage is not None:
            discount_rate = self.discount_percentage / Decimal('100')
            discounted_price = self.original_price * (Decimal('1') - discount_rate)
            self.current_price = discounted_price.quantize(Decimal('0.01'))  # Precise rounding
        else:
            self.current_price = self.original_price
        super().save(*args, **kwargs)

    @property
    def stock_status(self):
        return StockStatus.IN_STOCK if self.stock_count > 0 else StockStatus.OUT_OF_STOCK

class ProductImage(models.Model):
    """Multiple images for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image', folder='greenharvest_images/products', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)  # For SEO
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    """Product review model."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, (i*"⭐")) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=['product'])]

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"
