from django.contrib import admin
from .models import User, Category, Product, Order, OrderItem


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "role", "email", "phone","created_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name","created_at","is_active"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category", "stock","created_at","is_active","image"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ["product", "quantity", "price", "item_subtotal"]
    readonly_fields = ["price", "item_subtotal"]

    @admin.display(description="Subtotal")
    def item_subtotal(self, obj):
        if obj.pk:
            return obj.item_subtotal
        return "-"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_bill", "created_at"]
    fields = ["user", "status", "total_bill", "created_at"]
    readonly_fields = ["total_bill", "created_at"]
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "price","created_at","is_active"]
    fields = ["order", "product", "quantity", "price", "created_at", "is_active"]
    readonly_fields = ["price", "created_at"]
