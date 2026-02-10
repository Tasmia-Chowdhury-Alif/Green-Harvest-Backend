from abc import ABC, abstractmethod
from django.db import transaction
from orders.models import Order, OrderItem
from products.models import Product
from django.db.models import F

class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, request, cart, order):
        pass

    @abstractmethod
    def validate_payment(self, data):
        pass

    @staticmethod
    def process_order(cart, order):
        with transaction.atomic():
            # Lock products for update
            product_ids = cart.items.values_list('product__id', flat=True)
            products = Product.objects.select_for_update().filter(id__in=product_ids)
            product_map = {p.id: p for p in products}

            # Validate stock
            for item in cart.items.all():
                product = product_map[item.product.id]
                if item.quantity > product.stock_count:
                    order.status = 'cancelled'
                    order.save()
                    raise ValueError(f"Insufficient stock for {product.name}: {product.stock_count} available")

            # Update order status to 'order_received'
            order.status = 'order_received'
            order.save()

            # Create OrderItems and update stock
            for item in cart.items.all():
                product = product_map[item.product.id]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.current_price,
                )
                Product.objects.filter(pk=product.pk).update(stock_count=F('stock_count') - item.quantity)

            # Clear cart
            cart.items.all().delete()

            return True