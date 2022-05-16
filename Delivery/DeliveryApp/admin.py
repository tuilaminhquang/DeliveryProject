from django.contrib import admin
from .models import User, ShippingMethod,Order,Shipper,Customer, Status, Comment

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['shipper']
    list_filter = ['customer', 'created_date']


class ShipperAdmin(admin.ModelAdmin):
    class Meta:
       pass

class BiddingAdmin(admin.ModelAdmin):
    list_filter = ['shipper', 'created_date']


# Register your models here.
admin.site.register(ShippingMethod)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Shipper,ShipperAdmin)
admin.site.register(Customer)
admin.site.register(Status)
admin.site.register(Comment)
# admin.site.register(Bidding, BiddingAdmin)
# admin.site.register(Receipt)

