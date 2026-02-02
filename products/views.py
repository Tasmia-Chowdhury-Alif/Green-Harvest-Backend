from .models import Product, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer
from .filters import ProductFilter
from .pagination import ProductListPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse


@extend_schema(
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
            name='ordering',
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
                            "is_primary": True
                        }
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
                        "images": None
                    }
                ]
            }
        )
    ]
)
}
)
class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductListPagination 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['^name', 'description', '^category__name', '^brand__name', '^tags__name']  # ^ for starts-with (common practice for better search relevance)
    ordering_fields = ['created_at', 'current_price', 'average_rating', 'name']
    ordering = ['-created_at']  # Default: latest products first 

    def get_queryset(self):
        return Product.objects.select_related('category', 'brand').prefetch_related('images', 'tags')


@extend_schema(
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
                    "tags": ["organic", "fresh", "sweet"]
                },
                "images": [
                    {
                        "image": "https://res.cloudinary.com/yourcloud/image/upload/v1/greenharvest_images/products/apple1.jpg",
                        "alt_text": "Front view",
                        "is_primary": True
                    },
                    {
                        "image": "https://res.cloudinary.com/yourcloud/image/upload/v1/greenharvest_images/products/apple2.jpg",
                        "alt_text": "Side view",
                        "is_primary": False
                    }
                ]
            },
            response_only=True,
        )
    ]
)
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('images', 'tags')
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'


@extend_schema(
    summary="List all categories",
    description="Retrieve a list of categories with product counts (including subcategories via MPTT).",
    responses=CategorySerializer(many=True),
    examples=[
        OpenApiExample(
            name="Sample Category List Response",
            value=[
                {"id": 1, "name": "Fruits", "slug": "fruits", "product_count": 25},
                {"id": 2, "name": "Vegetables", "slug": "vegetables", "product_count": 38},
                {"id": 3, "name": "Dairy", "slug": "dairy", "product_count": 15}
            ],
            response_only=True,
        )
    ]
)
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()  # All categories (flat; extend to tree soon)
    serializer_class = CategorySerializer