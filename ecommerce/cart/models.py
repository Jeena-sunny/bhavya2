from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


from shop.models import Product


# Create your models here.
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)


    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.user.username
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.IntegerField(null= True)
    order_id = models.CharField(max_length=100,null= True)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(null= True, max_length=50)
    address = models.TextField(null= True)
    phone = models.CharField(max_length=15,null= True)
    is_ordered = models.BooleanField(default=False)
    delivery_status = models.CharField(default= "Pending",null= True,max_length=100)
    def __str__(self):
        return str(self.order_id)
class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.order.order_id

