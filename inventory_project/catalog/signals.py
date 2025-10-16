from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Product)
def ensure_stock_exists(sender, instance, created, **kwargs):
    if created:
        Stock.objects.get_or_create(product=instance)
