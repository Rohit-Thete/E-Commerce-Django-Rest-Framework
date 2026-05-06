from .models import *
from django.db import transaction
from rest_framework.exceptions import ValidationError


def create_order(user,items):
    total = 0

    with transaction.atomic():
        order = Order.objects.create(user = user,total_bill = 0)

        for item in items:
            product = item["product"]
            quantity = item["quantity"]
            price = product.price

            # TODO: use select for update to lock the product row to prevent race conditions
            # TODO: How client know which item out of stock?
            if product.stock < quantity:
                raise ValidationError({"error":"available stock is less than required Quantity"})
            
            obj = OrderItem.objects.create(
                order = order,
                product = product,
                quantity = quantity,
                price = price
            )
            # TODO: use item_subtotal
            total += quantity * price

            order.total_bill = total
            # TODO: only update total_bill field
            order.save()

            product.stock -= quantity
            # TODO: only update stock field
            product.save()

    return order


        
