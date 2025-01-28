from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        #otpravlaem yvedomlenie na pochty adminy
        send_mail(
            'new order',
            f'postypil novii zakaz #{instance.id}.',
            'noreply@example.com',
            ['admin@example.com'],
            
        )