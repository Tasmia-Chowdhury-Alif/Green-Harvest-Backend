import logging
import stripe
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.conf import settings

from cart.models import Cart
from orders.models import Order
from .gateway import PaymentGateway
from .sslcommerz_gateway import SSLCOMMERZGateway
from .stripe_gateway import StripeGateway
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


@extend_schema(exclude=True)
@method_decorator(csrf_exempt, name='dispatch')
class IPNView(APIView):
    def post(self, request):
        logger.info(f"SSLCOMMERZ IPN received: {request.data}")
        tran_id = request.data.get('tran_id')
        val_id = request.data.get('val_id')
        if Order.objects.filter(order_id=tran_id, payment_event_id=val_id).exists():
            return Response({'status': 'already processed'}, status=status.HTTP_200_OK)

        gateway = SSLCOMMERZGateway()
        success, error = gateway.validate_payment(request.data)
        if not success:
            return Response({'status': error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_id=tran_id)
            if order.status == 'order_received':
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            cart = Cart.objects.get(user=order.user)
            gateway.process_order(cart, order)
            order.payment_event_id = val_id
            order.save()
            logger.info(f"Order {order.id} processed successfully via SSLCOMMERZ")
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'status': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'status': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(exclude=True)
@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
            if Order.objects.filter(payment_event_id=event.id).exists():
                return Response({'status': 'already processed'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'status': 'invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response({'status': 'invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            if session.payment_status == 'paid':
                order_id = session.metadata.get('order_id')
                try:
                    order = Order.objects.get(order_id=order_id)
                    cart = Cart.objects.get(user=order.user)
                    gateway = StripeGateway()
                    success, error = gateway.validate_payment({'session_id': session.id})
                    if success:
                        gateway.process_order(cart, order)
                        order.payment_event_id = event.id
                        order.save()
                        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
                    return Response({'status': error}, status=status.HTTP_400_BAD_REQUEST)
                except Order.DoesNotExist:
                    return Response({'status': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({'status': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': 'unhandled event'}, status=status.HTTP_200_OK)



@csrf_exempt
def ssl_success(request):
    if request.method == "POST":
        order_id = request.POST.get("tran_id")
        return redirect(f"{settings.FRONTEND_BASE}/checkout/success?order_id={order_id}")
    return HttpResponse("Method not allowed", status=405)

@csrf_exempt
def ssl_fail(request):
    if request.method == "POST":
        order_id = request.POST.get("tran_id")
        return redirect(f"{settings.FRONTEND_BASE}/checkout/failed?order_id={order_id}")
    return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def ssl_cancel(request):
    if request.method == "POST":
        order_id = request.POST.get("tran_id")
        return redirect(f"{settings.FRONTEND_BASE}/checkout/cancelled?order_id={order_id}")
    return HttpResponse("Method not allowed", status=405)


# @csrf_exempt
# def payment_success(request):
#     session_id = request.GET.get('session_id')
#     context = {}
#     if session_id:
#         try:
#             session = stripe.checkout.Session.retrieve(session_id)
#             order_id = session.metadata.get('order_id')
#             frontend_url = f"{settings.FRONTEND_BASE}/checkout/success?order_id={order_id}"
#         except Exception as e:
#             context['error'] = str(e)
#     return HttpResponseRedirect(frontend_url)

# @csrf_exempt
# def payment_fail(request):
#     session_id = request.GET.get('session_id')
#     context = {}
#     if session_id:
#         try:
#             session = stripe.checkout.Session.retrieve(session_id)
#             order_id = session.metadata.get('order_id')
#             frontend_url = f"{settings.FRONTEND_BASE}/checkout/failed?order_id={order_id}"
#         except Exception as e:
#             context['error'] = str(e)
#     return HttpResponseRedirect(frontend_url)

# @csrf_exempt
# def payment_cancel(request):
#     session_id = request.GET.get('session_id')
#     context = {}
#     if session_id:
#         try:
#             session = stripe.checkout.Session.retrieve(session_id)
#             order_id = session.metadata.get('order_id')
#             frontend_url = f"{settings.FRONTEND_BASE}/checkout/cancled?order_id={order_id}"
#         except Exception as e:
#             context['error'] = str(e)
#     return HttpResponseRedirect(frontend_url)