import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_by_category')  # ?category=slug (includes subcatsagory)
    min_price = django_filters.NumberFilter(field_name='current_price', lookup_expr='gte')  # ?min_price=10
    max_price = django_filters.NumberFilter(field_name='current_price', lookup_expr='lte')  # ?max_price=50
    rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')  # ?rating=4 (min rating)
    tags = django_filters.CharFilter(method='filter_by_tags')  # ?tags=apple,green (comma-separated, any match)

    def filter_by_category(self, queryset, name, value):
        if value:
            try:
                cat = Category.objects.get(slug=value)
                descendants = cat.get_descendants(include_self=True)
                queryset = queryset.filter(category__in=descendants)
            except Category.DoesNotExist:
                pass
        return queryset

    def filter_by_tags(self, queryset, name, value):
        if value:
            tags_slugs = [t.strip() for t in value.split(',')]
            queryset = queryset.filter(tags__slug__in=tags_slugs).distinct()
        return queryset

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'rating']