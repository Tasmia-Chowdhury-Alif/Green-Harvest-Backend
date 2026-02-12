from django.urls import path
from .views import IPNView, StripeWebhookView, ssl_success, ssl_fail, ssl_cancel

app_name = 'payments'

urlpatterns = [
    path('ipn/', IPNView.as_view(), name='sslcommerz-ipn'),
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('ssl-success/', ssl_success, name='ssl-success'),
    path('ssl-fail/', ssl_success, name='ssl-fail'),
    path('ssl-cancel/', ssl_success, name='ssl-cancel'),
]
