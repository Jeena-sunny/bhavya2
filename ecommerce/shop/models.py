

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import random
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=11)
    gender = models.CharField(max_length=11)

    is_verified = models.BooleanField(default=False)
    otp=models.CharField(max_length=11,null=True)
class Category(models.Model):
    name = models.CharField(max_length=11)
    discription = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=11)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    discription = models.CharField(max_length=100)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

