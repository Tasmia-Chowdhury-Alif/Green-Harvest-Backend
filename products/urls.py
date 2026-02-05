from django.urls import path
from .views import BrandListView, CategoryLeafListView, ProductListView, ProductDetailView, CategoryListView, ReviewCreateView, ReviewDetailView, ReviewListView, TagListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/leaf/', CategoryLeafListView.as_view(), name='category-leaf-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('products/<int:product_id>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('products/<int:product_id>/reviews/<int:id>/', ReviewDetailView.as_view(), name='review-detail'),
]
