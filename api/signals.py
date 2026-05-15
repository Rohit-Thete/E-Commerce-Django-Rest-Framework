from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import User, Order, OrderStatus
from .task import send_welcome_email, send_order_confirmation_email, send_order_cancellation_email, send_order_delivered_email



@receiver(pre_save, sender=User)
def pre_save_email_validation_signal(sender,instance,**kwargs):
    if instance.email:
        instance.email = instance.email.lower().strip()
    

@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda : send_welcome_email.delay(instance.username, instance.email))
        

@receiver(post_save, sender=Order)
def send_order_confirmation_signal(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda : send_order_confirmation_email.delay(instance.user.username, instance.user.email, instance.id))
    else:

        if  instance.status == OrderStatus.CANCELLED:
            send_order_cancellation_email.delay(instance.user.username, instance.user.email, instance.id) 

        elif instance.status == OrderStatus.DELIVERED:
            send_order_delivered_email.delay(instance.user.username, instance.user.email, instance.id)


# @receiver(post_save,sender=Order)
# def send_order_cancellation_signal(sender, instance, created, **kwargs):
#     if not created and instance.status == OrderStatus.CANCELLED:
#         send_order_cancellation_email.delay(instance.user.username, instance.user.email, instance.id)

# @receiver(post_save,sender=Order)
# def send_order_delivered_signal(sender, instance, created, **kwargs):
#     if not created and instance.status == OrderStatus.DELIVERED:
#         send_order_delivered_email.delay(instance.user.username, instance.user.email, instance.id)


