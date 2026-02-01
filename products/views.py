from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer
from .filters import ProductFilter


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category', 'brand', 'tags'] 

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand').prefetch_related('images', 'tags')
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'latest':
            return queryset.order_by('-created_at')
        elif sort_by == 'price_low_to_high':
            return queryset.order_by('current_price')
        elif sort_by == 'price_high_to_low':
            return queryset.order_by('-current_price')
        elif sort_by == 'rating':
            return queryset.order_by('-average_rating')
        elif sort_by == 'name':
            return queryset.order_by('name')
        return queryset.order_by('-created_at')  # Default: latest

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('images', 'tags')
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()  # All categories (flat; extend to tree soon)
    serializer_class = CategorySerializer