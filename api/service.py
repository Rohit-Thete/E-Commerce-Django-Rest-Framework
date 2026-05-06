from .models import *
from django.db import transaction
from rest_framework.exceptions import ValidationError


def create_order(user,items):
    total = 0

    with transaction.atomic():
        order = Order.objects.create(user = user,total_bill = 0)

        for item in items:
            product = Product.objects.select_for_update().get(id=item["product"].id)
            quantity = item["quantity"]
            price = product.price

            # TODO: use select for update to lock the product row to prevent race conditions
            # TODO: How client know which item out of stock?
            if product.stock < quantity:
                raise ValidationError({"error":f"available stock for {product.name} is less than required Quantity"})
            
            obj = OrderItem.objects.create(
                order = order,
                product = product,
                quantity = quantity,
                price = price
            )
            # TODO: use item_subtotal
            total += obj.item_subtotal

            order.total_bill = total
            # TODO: only update total_bill field
            order.save(update_fields=["total_bill"])

            product.stock -= quantity
            # TODO: only update stock field
            product.save(update_fields=["stock"])

    return order


        
