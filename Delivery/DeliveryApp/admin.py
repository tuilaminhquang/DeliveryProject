from django.contrib import admin
from .models import User, ShippingMethod,Order,Shipper,Customer, Status


class ShipperAdmin(admin.ModelAdmin):
    class Meta:
       pass

# Register your models here.
admin.site.register(ShippingMethod)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Shipper,ShipperAdmin)
admin.site.register(Customer)
admin.site.register(Status)

