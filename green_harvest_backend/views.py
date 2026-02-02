from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema

class ApiRootView(APIView):
    @extend_schema(exclude=True)  # Excludes from schema
    def get(self, request, format=None):
        return Response({
            'Message': 'Welcome to Green Harvest API',
            'Download Schema': reverse('schema', request=request, format=format),
            'Swagger Documentation UI': reverse('swagger-ui', request=request, format=format),
            'Redoc Documentation UI': reverse('redoc', request=request, format=format),
        })