from django.urls import path
from .views import OrderListAPIView, OrderDetailAPIView, CheckoutAPIView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('', OrderListAPIView.as_view(), name='order-list'),
    path('<str:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
