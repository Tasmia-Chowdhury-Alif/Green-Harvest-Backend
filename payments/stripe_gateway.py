import stripe
from django.conf import settings
from .gateway import PaymentGateway
from rest_framework import status
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class StripeGateway(PaymentGateway):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def initiate_payment(self, request, cart, order):
        try:
            line_items = []
            for item in cart.items.all():
                primary_image = item.product.images.filter(is_primary=True).first() or item.product.images.first()
                image_url = primary_image.image.url if primary_image else None
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                            'images': [image_url] if image_url else [],
                        },
                        'unit_amount': int(item.product.current_price * 100),
                    },
                    'quantity': item.quantity,
                })
            
            frontend = settings.FRONTEND_BASE

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f"{frontend}/checkout/success?order_id={order.order_id}",
                cancel_url=f"{frontend}/checkout/cancel?order_id={order.order_id}",
                metadata={'order_id': order.order_id},
            )
            return {'payment_url': session.url}, status.HTTP_200_OK
        except stripe.error.StripeError as e:
            logger.error(str(e))
            return {'error': str(e)}, status.HTTP_400_BAD_REQUEST

    def validate_payment(self, data):
        try:
            session_id = data.get('session_id')
            session = stripe.checkout.Session.retrieve(session_id)
            return session.payment_status == 'paid', None if session.payment_status == 'paid' else 'Payment incomplete'
        except stripe.error.StripeError as e:
            logger.error(str(e))
            return False, str(e)