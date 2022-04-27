from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Shipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    identity_number = models.CharField(max_length=20, null=True,)

    def __str__(self):
        return self.user.username




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
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Order(ModelBase):
    order_name = models.CharField(max_length=100, null=False)
    note = models.CharField(max_length=255)

    image = models.ImageField(null=True, blank=True, upload_to='orders/%Y/%m')
    shipping_method = models.ForeignKey(ShippingMethod,
                                        null=True,
                                        on_delete=models.SET_NULL,
                                        related_name='order',
                                        )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper,null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(Status,null=True, default=1, on_delete=models.SET_NULL)


    def __str__(self):
        return self.order_name



