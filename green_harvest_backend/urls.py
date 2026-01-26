from django.contrib import admin
from django.urls import path, include
from .views import ApiRootView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # API Root View at project root
    path('', ApiRootView.as_view(), name='api-root'),

    path('admin/', admin.site.urls),

    path("api/auth/", include("djoser.urls")),  # /auth/users/, /auth/users/me/
    path("api/auth/", include("djoser.urls.jwt")),  # /auth/jwt/create/, etc.

    # Swagger & Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
