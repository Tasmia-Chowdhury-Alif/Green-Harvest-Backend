from .models import Product, Category, Tag, Brand, Review
from .serializers import (ProductListSerializer, ProductDetailSerializer, CategorySerializer, CategoryRootSerializer, ReviewWriteSerializer, TagSerializer, BrandSerializer, ReviewSerializer,)
from .filters import ProductFilter
from .pagination import ProductListPagination
from .permissions import IsReviewOwnerOrReadOnly
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse


@extend_schema(
    tags=["Products"],
    summary="List all products",
    description=(
        "Retrieve a paginated list of products with filtering, searching, and ordering.\n\n"
        "Supports hierarchical category filtering (includes subcategories).\n\n"
        "**Pagination**: ?page=1&page_size=20 (defaults to 20 items per page).\n\n"
        "**Ordering**: Use ?ordering=field or ?ordering=-field\n\n"
        "**Supported fields**: created_at, current_price, average_rating, name\n\n"
        "**Examples**:\n\n"
        "  ?ordering=-created_at          → newest first (default)\n\n"
        "  ?ordering=current_price        → cheapest first\n\n"
        "  ?ordering=-current_price       → most expensive first\n\n"
        "  ?ordering=-average_rating      → highest rated first\n\n"
        "  ?ordering=name                 → alphabetical A-Z"
    ),
    # parameters=[],  # Auto-detected by spectacular (e.g., ?search=, ?ordering=, filters from ProductFilter)
    parameters=[
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=['created_at', '-created_at', 'current_price', '-current_price', 'average_rating', '-average_rating', 'name', '-name'],
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="Paginated list of products",
            response=ProductListSerializer(many=True),
            examples=[
                OpenApiExample(
                    "Successful response example",
                    value={
                        "count": 42,
                        "next": "http://127.0.0.1:8000/api/products/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 15,
                                "slug": "organic-red-apples-1kg",
                                "name": "Organic Red Apples 1kg",
                                "current_price": "320.00",
                                "original_price": "380.00",
                                "discount_percentage": 15.79,
                                "average_rating": 4.6,
                                "stock_status": "IN_STOCK",
                                "images": {
                                    "image": "https://res.cloudinary.com/.../apples-primary.jpg",
                                    "alt_text": "Fresh organic red apples",
                                    "is_primary": True,
                                },
                            },
                            {
                                "id": 7,
                                "slug": "banana-cavendish-1kg",
                                "name": "Banana Cavendish 1kg",
                                "current_price": "180.00",
                                "original_price": "180.00",
                                "discount_percentage": None,
                                "average_rating": 4.2,
                                "stock_status": "IN_STOCK",
                                "images": None,
                            },
                        ],
                    },
                )
            ],
        )
    },
)
class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['^name', 'description', '^category__name', '^brand__name', '^tags__name']  # ^ for starts-with (common practice for better search relevance)
    ordering_fields = ['created_at', 'current_price', 'average_rating', 'name']
    ordering = ['created_at']  # Default: Oldest products first 

    @method_decorator(cache_page(60 * 60, key_prefix='product_list'))
    def list(self, request, *args, ** kwargs):
        return super().list(request, *args, ** kwargs)

    def get_queryset(self):
        # import time
        # time.sleep(10)
        return Product.objects.select_related('category', 'brand').prefetch_related('images', 'tags')


@extend_schema(
    tags=["Products"],
    summary="Retrieve a single product",
    description="Get detailed information for a product by its slug, including images, reviews count, and additional info.",
    responses=ProductDetailSerializer,
    examples=[
        OpenApiExample(
            name="Sample Product Detail Response",
            value={
                "id": 1,
                "slug": "fresh-apple",
                "name": "Fresh Apple",
                "sku": "GH-A1B2C3D4",
                "current_price": "45.00",
                "original_price": "60.00",
                "discount_percentage": "25.00",
                "average_rating": 4.5,
                "reviews_count": 12,
                "stock_status": "IN_STOCK",
                "category": "Fruits",
                "description": "Crisp and juicy red apples, freshly harvested.",
                "additional_info": {
                    "weight": "1 kg",
                    "color": "Red",
                    "type": "Fruit",
                    "stock_count": 150,
                    "tags": ["organic", "fresh", "sweet"],
                },
                "images": [
                    {
                        "image": "https://res.cloudinary.com/yourcloud/image/upload/v1/greenharvest_images/products/apple1.jpg",
                        "alt_text": "Front view",
                        "is_primary": True,
                    },
                    {
                        "image": "https://res.cloudinary.com/yourcloud/image/upload/v1/greenharvest_images/products/apple2.jpg",
                        "alt_text": "Side view",
                        "is_primary": False,
                    },
                ],
            },
            response_only=True,
        )
    ],
)
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('images', 'tags')
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


@extend_schema(
    tags=["Categories"],
    summary="List all categories (hierarchical tree)",
    description=(
        "Retrieve a hierarchical list of categories starting from roots, with product counts (including subcategories via MPTT) "
        "and nested children. Ideal for building nested menus or category trees in the frontend."
    ),
    responses=CategorySerializer(many=True),
    examples=[
        OpenApiExample(
            name="Sample Hierarchical Category Response",
            value=[
                {
                    "id": 1, "name": "Fruits", "slug": "fruits", "product_count": 25,
                    "children": [
                        {"id": 4, "name": "Apples", "slug": "apples", "product_count": 10, "children": []},
                        {"id": 5, "name": "Berries", "slug": "berries", "product_count": 15, "children": []}
                    ]
                },
                {"id": 2, "name": "Vegetables", "slug": "vegetables", "product_count": 38, "children": []},
                {"id": 3, "name": "Dairy", "slug": "dairy", "product_count": 15, "children": []}
            ],
            response_only=True,
        )
    ],
)
class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)  # Starting from root categories for tree
    serializer_class = CategorySerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 60, key_prefix='category_list'))
    def list(self, request, *args, ** kwargs):
        return super().list(request, *args, ** kwargs)


@extend_schema(
    tags=["Categories"],
    summary="List root categories shop filtering",
    description=(
        "Returns top-level (root/parent) categories with product counts including all subcategories. "
        "Recommended for the product shop page sidebar filter. "
        "When user selects a category (by slug), the /products/ endpoint with ?category=slug "
        "will automatically include all child products thanks to MPTT."
    ),
    responses=CategoryRootSerializer(many=True),
    examples=[
        OpenApiExample(
            name="Sample Leaf Category Response",
            value=[
                {"id": 4, "name": "Apples", "slug": "apples", "product_count": 10},
                {"id": 5, "name": "Berries", "slug": "berries", "product_count": 15},
                {"id": 6, "name": "Leafy Greens", "slug": "leafy-greens", "product_count": 20}
            ],
            response_only=True,
        )
    ],
)
class CategoryRootListView(ListAPIView):
    serializer_class = CategoryRootSerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 60, key_prefix='category_root_list'))
    def list(self, request, *args, ** kwargs):
        return super().list(request, *args, ** kwargs)

    def get_queryset(self):
        # Only root categories (no parent) that are active
        return Category.objects.filter(parent=None, is_active=True)


@extend_schema(
    tags=["Tags"],
    summary="List all tags",
    description="Retrieve a list of all tags used for products.",
    responses=TagSerializer(many=True),
    examples=[
        OpenApiExample(
            name="Sample Tags Response",
            value=[
                {"id": 1, "name": "organic", "slug": "organic"},
                {"id": 2, "name": "fresh", "slug": "fresh"},
            ],
            response_only=True,
        )
    ],
)
class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


@extend_schema(
    tags=["Brands"],
    summary="List all brands",
    description="Retrieve a list of all brands with their images.",
    responses=BrandSerializer(many=True),
    examples=[
        OpenApiExample(
            name="Sample Brands Response",
            value=[
                {
                    "id": 1, "name": "Organic Farms", 
                    "image": "https://res.cloudinary.com/.../organic-farms-logo.jpg"
                },
                {"id": 2, "name": "Fresh Harvest", "image": None},
            ],
            response_only=True,
        )
    ],
)
class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@extend_schema(
    tags=["Reviews"],
    summary="List reviews for a product",
    description=(
        "Retrieve paginated reviews for a specific product by ID. Supports pagination for 'load more' functionality "
        "(e.g., ?page=2). Each review includes user image, full name, rating, comment, and formatted time (e.g., '5 min ago' or date)."
    ),
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID of the product to fetch reviews for.",
        ),
    ],
    responses=ReviewSerializer(many=True),
    examples=[
        OpenApiExample(
            name="Sample Reviews Response",
            value=[
                {
                    "id": 1,
                    "user": {"full_name": "John Doe", "email": "test1@gmail.com", "image": "https://res.cloudinary.com/.../user.jpg"},
                    "rating": 5,
                    "comment": "Great product!",
                    "created_at": "2 hours ago"
                },
                {
                    "id": 2,
                    "user": {"full_name": "Jane Smith", "email": "test2@gmail.com", "image": None},
                    "rating": 4,
                    "comment": "Good quality.",
                    "created_at": "2026-01-15",
                },
            ],
            response_only=True,
        )
    ],
)
class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = None
    filter_backends = []

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id).select_related('user', 'user__profile').order_by('-created_at')


@extend_schema(
    tags=["Reviews"],
    summary="Create a review for a product",
    description=(
        "Authenticated users can submit one review per product.\n"
        "Duplicate reviews are prevented."
    ),
    request=ReviewWriteSerializer,
    responses={
        201: ReviewSerializer,
        400: OpenApiResponse(description="Validation error or already reviewed"),
    },
)
class ReviewCreateView(generics.CreateAPIView):
    """
    POST: Create a new review for a product (authenticated user only)
    """

    serializer_class = ReviewWriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs["product_id"])
        # Prevent duplicate reviews (one per user per product)
        if Review.objects.filter(product=product, user=self.request.user).exists():
            raise ValidationError({"detail": "You have already reviewed this product."})

        serializer.save(product=product, user=self.request.user)


@extend_schema(
    tags=["Reviews"],
    summary="Retrieve, update or delete a review",
    description=(
        "• **GET**: Retrieve details of a specific review\n"
        "• **PUT / PATCH**: Update your own review (rating and/or comment)\n"
        "• **DELETE**: Delete your own review\n\n"
        "Only the review's author can modify or delete it."
    ),
    request=ReviewWriteSerializer,  # for PUT/PATCH
    responses={
        200: ReviewSerializer,
        204: OpenApiResponse(description="Review deleted successfully"),
        403: OpenApiResponse(description="You do not have permission (not the owner)"),
        404: OpenApiResponse(description="Review not found"),
    },
    methods=["GET", "PUT", "PATCH", "DELETE"],  # important for multi-method view
)
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single review (if public/owned)
    PUT/PATCH: Update review (only owner)
    DELETE: Delete review (only owner)
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer  # read serializer
    permission_classes = [IsAuthenticated, IsReviewOwnerOrReadOnly]
    lookup_field = "id"  # or 'pk'

    def get_queryset(self):
        # Optional: can restrict to product if needed
        product_id = self.kwargs.get("product_id")
        if product_id:
            return super().get_queryset().filter(product_id=product_id)
        return super().get_queryset()

    def perform_destroy(self, instance):
        # Optional: extra logic before delete
        super().perform_destroy(instance)

