

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