from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES =(('admin','Admin'),('customer','Customer'))
    first_name = None
    last_name = None
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='customer')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,unique=True)

    REQUIRED_FIELDS =["email","phone"]

    class Meta:
        ordering=["username"]

    def __str__(self):
        return f"{self.username} - {self.email}"


class Category(models.Model):
    name = models.CharField(max_length=20,unique=True) 

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    
    def __str__(self):
        return f"{self.name} - {self.category} - {self.stock} - {self.price}"
    

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,through='OrderItem')
    date_created = models.DateTimeField(auto_now_add=True)
    total_bill = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.date_created}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    @property
    def item_subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.order} - {self.product} - {self.quantity} - {self.price}"




