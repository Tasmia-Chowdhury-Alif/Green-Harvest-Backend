from django.urls import path
from .views import IPNView, StripeWebhookView

app_name = 'payments'

urlpatterns = [
    path('ipn/', IPNView.as_view(), name='sslcommerz-ipn'),
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
