from rest_framework.pagination import PageNumberPagination

class ProductListPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = "page_size"   # optional (allows frontend override)
    max_page_size = 30                     # safety limit
