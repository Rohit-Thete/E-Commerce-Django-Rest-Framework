
from django.db import models
from django.contrib.auth.models import AbstractUser


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# Create your models here.
class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    CUSTOMER = "customer", "Customer"


class OrderStatus(models.TextChoices):
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    DELIVERED = "delivered", "Delivered"


class User(AbstractUser, AbstractBaseModel):
    first_name = None
    last_name = None
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)

    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} - {self.email}"


class Category(AbstractBaseModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Product(AbstractBaseModel):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.category} - {self.stock} - {self.price}"


class Order(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        choices=OrderStatus.choices, default=OrderStatus.CONFIRMED
    )

    def update_total_bill(self):
        total = sum(item.item_subtotal for item in self.items.all())
        self.total_bill = total
        self.save(update_fields=["total_bill"])

    def __str__(self):
        return f"{self.user} - {self.created_at} - {self.status} - {self.total_bill}"


class OrderItem(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def item_subtotal(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if self.product_id:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.order.update_total_bill()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total_bill()

    def __str__(self):
        return f"{self.order} - {self.product} - {self.quantity} - {self.price}"
