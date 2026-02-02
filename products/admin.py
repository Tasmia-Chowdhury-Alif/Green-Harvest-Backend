from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Tag, Brand, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Start with 1 empty form
    fields = ('image', 'alt_text', 'is_primary')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)


class StockStatusFilter(admin.SimpleListFilter):
    title = 'Stock Status'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):
        return (
            ('in_stock', 'In Stock'),
            ('out_of_stock', 'Out of Stock'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(stock_count__gt=0)
        if self.value() == 'out_of_stock':
            return queryset.filter(stock_count=0)
        return queryset


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected as inactive"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def display_stock_status(self, obj):
        return obj.stock_status
    
    display_stock_status.short_description = "Stock Status"

    list_display = ('name', 'sku', 'original_price', 'current_price', 'display_stock_status', 'brand', 'category', 'average_rating', 'reviews_count')
    search_fields = ('name', 'sku', 'description')
    list_filter = ('brand', 'category', StockStatusFilter)

    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('current_price', 'average_rating', 'reviews_count', 'display_stock_status', 'created_at')
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'sku', 'brand', 'category', 'tags')}),
        ('Pricing', {'fields': ('original_price', 'discount_percentage', 'current_price')}),
        ('Details', {'fields': ('description', 'weight', 'color', 'type')}),
        ('Inventory', {'fields': ('stock_count', 'display_stock_status')}),
        ('Ratings', {'fields': ('average_rating', 'reviews_count')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    inlines = [ProductImageInline, ReviewInline]
    raw_id_fields = ('category', 'brand')
    actions = ['out_of_stock', 'in_stock']

    def out_of_stock(self, request, queryset):
        queryset.update(stock_count=0)
    out_of_stock.short_description = "Set selected to out of stock"

    def in_stock(self, request, queryset):
        queryset.update(stock_count=10)  # default stock
    in_stock.short_description = "Set selected to in stock"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__email')
    list_filter = ('rating',)
    readonly_fields = ('created_at', 'updated_at')