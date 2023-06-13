from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Extended User Table
class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

# Product Info table
class ProductTable(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    total_peice = models.FloatField()
    stock_status = models.CharField(max_length=15)

    def __str__(self):
        return self.name


