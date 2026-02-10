from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from .models import Order
from cart.models import Cart
from .serializers import OrderSerializer
from payments.sslcommerz_gateway import SSLCOMMERZGateway
from payments.stripe_gateway import StripeGateway
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Checkout - Create order and initiate payment",
    description="Creates a pending order with shipping address and starts payment process",
    tags=["Checkout"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "payment_method": {
                    "type": "string",
                    "enum": ["sslcommerz", "stripe"],
                    "default": "sslcommerz"
                },
                "shipping_address": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "company_name": {"type": "string", "nullable": True},
                        "street_address": {"type": "string"},
                        "city": {"type": "string"},
                        "country": {"type": "string"},
                        "postcode": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "phone_number": {"type": "string"},
                        "order_notes": {"type": "string", "nullable": True},
                    },
                    "required": ["first_name", "last_name", "street_address", "city", "country", "postcode", "email", "phone_number"]
                }
            },
            "required": ["shipping_address"]
        }
    },
    responses={
        200: {"type": "object", "properties": {"payment_url": {"type": "string"}}},
        400: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    examples=[
        OpenApiExample(
            "Example request",
            value={
                "payment_method": "stripe",
                "shipping_address": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "street_address": "123 Dhaka St",
                    "city": "Dhaka",
                    "country": "Bangladesh",
                    "postcode": "1200",
                    "email": "john@example.com",
                    "phone_number": "+880123456789",
                    "order_notes": "Deliver in evening"
                }
            }
        )
    ]
)
class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_method = request.data.get('payment_method', 'sslcommerz').lower()
        address = request.data.get('shipping_address')

        if not address or not all(key in address for key in ['first_name', 'last_name', 'street_address', 'city', 'country', 'postcode', 'email', 'phone_number']):
            return Response({'error': 'Incomplete shipping address'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
            if not cart.items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            # Early stock validation
            for item in cart.items.all():
                if item.quantity > item.product.stock_count:
                    return Response(
                        {'error': f'Insufficient stock for {item.product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create pending order
            order = Order.objects.create(
                user=request.user,
                payment_method=payment_method,
                **address,
            )
            order.calculate_totals(cart)
            if order.total <= Decimal('0'):  # Edge case: zero total
                return Response({'error': 'Order total must be positive'}, status=status.HTTP_400_BAD_REQUEST)
            order.save()

            # Select and initiate gateway
            gateways = {
                'sslcommerz': SSLCOMMERZGateway,
                'stripe': StripeGateway,
            }
            gateway_class = gateways.get(payment_method)
            if not gateway_class:
                return Response({'error': 'Invalid payment method'}, status=status.HTTP_400_BAD_REQUEST)

            gateway = gateway_class()
            response_data, status_code = gateway.initiate_payment(request, cart, order)
            return Response(response_data, status=status_code)

        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@extend_schema(summary="List user's order history", tags=["Orders"])
class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.none()
    permission_classes = [IsAuthenticated]
    filter_backends = []

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

@extend_schema(summary="Retrieve order details", tags=["Orders"])
class OrderDetailAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)