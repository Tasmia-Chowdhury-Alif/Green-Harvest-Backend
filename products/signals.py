from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from .models import ProductImage, Review

# Signals for unique is_primary
@receiver(pre_save, sender=ProductImage)
def ensure_unique_primary_image(sender, instance, **kwargs):
    if instance.is_primary:
        # Set all other images for this product to non-primary
        ProductImage.objects.filter(product=instance.product).exclude(pk=instance.pk).update(is_primary=False)

# Signals for updating product ratings/count (on review save/delete)
def update_product_ratings(product):
    reviews = product.reviews.all()
    if reviews.exists():
        avg = round(sum(r.rating for r in reviews) / reviews.count(), 1)
        count = reviews.count()
    else:
        avg = 0.0
        count = 0
    product.average_rating = avg
    product.reviews_count = count
    product.save(update_fields=['average_rating', 'reviews_count'])

@receiver(post_save, sender=Review)
def post_save_review(sender, instance, **kwargs):
    update_product_ratings(instance.product)

@receiver(post_delete, sender=Review)
def post_delete_review(sender, instance, **kwargs):
    update_product_ratings(instance.product)
    