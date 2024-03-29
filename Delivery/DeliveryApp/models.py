from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default='', blank=True)

    def __str__(self):
        return self.user.username


class Shipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identity_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username




class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Order(ModelBase):
    order_name = models.CharField(max_length=100, null=False)
    note = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='orders/%Y/%m')
    from_address = models.TextField(max_length=100, null=False)
    to_address = models.TextField(max_length=100, null=False)
    km = models.FloatField(default=1)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name="orders")
    status = models.ForeignKey(Status,null=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.order_name

class ActionBase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('customer', 'shipper')
        abstract=True

class RatingShipper(ActionBase):
    rate = models.SmallIntegerField(default=0)



class Bidding(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bidding')
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    bid = models.IntegerField(default=0)

    class Meta:
        unique_together=('order', 'shipper')
    def __str__(self):
        return self.order.order_name


class Comment(ModelBase):
    content = models.TextField()
    shipper = models.ForeignKey(Shipper,
                               related_name='comments',
                               on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Receipt(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name='receipts')
    price = models.IntegerField(default=0)
    def __str__(self):
        return self.order.order_name



