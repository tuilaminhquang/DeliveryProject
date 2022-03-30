from django.contrib import admin
from .models import User, ShippingMethod,Order

# Register your models here.
admin.site.register(ShippingMethod)
admin.site.register(Order)
admin.site.register(User)

