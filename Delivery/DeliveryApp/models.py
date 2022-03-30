from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    is_shipper = models.BooleanField(default=False)
    iden_no = models.TextField(max_length=100, null=True)







class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ShippingMethod(ModelBase):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Order(ModelBase):
    order_name = models.CharField(max_length=100, null=False)
    note = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to='orders/%Y/%m')
    shipping_method = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.order_name



