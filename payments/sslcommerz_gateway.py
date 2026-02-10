import requests
from decimal import Decimal
from django.conf import settings
from .gateway import PaymentGateway
from rest_framework import status

class SSLCOMMERZGateway(PaymentGateway):
    def initiate_payment(self, request, cart, order):
        # Fetch exchange rate: 1 USD to BDT
        try:
            response = requests.get("https://open.exchangerate-api.com/v6/latest/USD")
            response.raise_for_status()
            data = response.json()
            rate = Decimal(str(data['rates']['BDT']))
        except Exception as e:
            rate = Decimal(settings.get('BDT_FALLBACK_RATE', '122'))

        total_bdt = order.total * rate

        frontend = settings.FRONTEND_BASE
        backend = settings.BASE_URL

        payload = {
            'store_id': settings.SSLC_STORE_ID,
            'store_passwd': settings.SSLC_STORE_PASS,
            'total_amount': float(total_bdt),
            'currency': 'BDT',
            'tran_id': order.order_id,
            'success_url': f"{frontend}/checkout/success?order_id={order.order_id}",
            'fail_url': f"{frontend}/checkout/failed?order_id={order.order_id}",
            'cancel_url': f"{frontend}/checkout/cancel?order_id={order.order_id}",
            'ipn_url': f"{backend}/payments/ipn/",
            'cus_name': f"{order.first_name} {order.last_name}",
            'cus_email': order.email,
            'cus_phone': order.phone_number,
            'cus_add1': order.street_address,
            'cus_city': order.city,
            'cus_postcode': order.postcode,
            'cus_country': order.country,
            'shipping_method': 'NO',
            'num_of_item': cart.items.count(),
            'product_name': ', '.join([item.product.name for item in cart.items.all()]),
            'product_category': 'Groceries',
            'product_profile': 'physical-goods',
        }

        url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php" if settings.SSLC_IS_SANDBOX else "https://securepay.sslcommerz.com/gwprocess/v4/api.php"

        try:
            resp = requests.post(url, data=payload)
            resp.raise_for_status()
            data = resp.json()
            if data.get('status') == 'SUCCESS':
                return {'payment_url': data['GatewayPageURL']}, status.HTTP_200_OK
            return {'error': data.get('failedreason', 'Payment initiation failed')}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {'error': str(e)}, status.HTTP_400_BAD_REQUEST

    def validate_payment(self, data):
        tran_id = data.get('tran_id')
        val_id = data.get('val_id')
        if not tran_id or not val_id:
            return False, 'Missing data'

        from orders.models import Order
        try:
            order = Order.objects.get(order_id=tran_id)
        except Order.DoesNotExist:
            return False, 'Order not found'

        url = "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php" if settings.SSLC_IS_SANDBOX else "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php"
        params = {
            'val_id': val_id,
            'store_id': settings.SSLC_STORE_ID,
            'store_passwd': settings.SSLC_STORE_PASS,
            'format': 'json',
        }

        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            validation = resp.json()
            if validation.get('status') == 'VALID':
                return True, None
            order.status = 'cancelled'
            order.save()
            return False, 'Invalid payment'
        except Exception as e:
            order.status = 'cancelled'
            order.save()
            return False, str(e)