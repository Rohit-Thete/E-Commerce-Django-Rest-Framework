from django.core.mail import send_mail
import resend
from celery import shared_task
from django.conf import settings


@shared_task
def send_welcome_email(username, email):

    send_mail(
        subject="Welcome",
        message=f"Hello {username}, welcome to our website!",
        from_email="rohitthete.512@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def send_order_confirmation_email(username, email, orderid):
    send_mail(
        subject="Order confirmation",
        message=f"Hello {username} your order has been confirmed with order id {orderid} you can check your order details by login in your account",
        from_email="rohitthete.512@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

@shared_task
def send_order_cancellation_email(username, email, orderid):
    send_mail(
        subject="Order Cancellation",
        message=f"Hello {username} your order has been cancelled with order id {orderid} you can check your order details by login in your account",
        from_email="rohitthete.512@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

@shared_task
def send_order_delivered_email(username, email, orderid):
    send_mail(
        subject="Order Delivered Successfully",
        message=f"Hello {username} your order has been delivered successfully with order id {orderid} you can check your order details by login in your account",
        from_email="rohitthete.512@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

# @shared_task
# def send_welcome_email(username, email):

#     resend.api_key = settings.RESEND_API_KEY

#     resend.Emails.send({
#         "from": "onboarding@resend.dev",
#         "to": email,
#         "subject": "Welcome",
#         "html": f"<h1>Hello {username} Welcome to our Website. Hope you enjoy our platform </h1>",
#     })


# @shared_task
# def send_order_confirmation_email(username, email,orderid):

#     resend.api_key = settings.RESEND_API_KEY

#     resend.Emails.send({
#         "from": "onboarding@resend.dev",
#         "to": email,
#         "subject": "Order Confirmation",
#         "html": f"<h1>Hello {username} this is your order id {orderid} you can check your order detail by login in your account </h1>",
#     })
