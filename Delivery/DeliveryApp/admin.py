from django.contrib import admin
from .models import User,Order,Shipper,Customer, Status, Comment, Bidding, RatingShipper
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['customer', 'created_date']
    readonly_fields = ['image_view']

    def image_view(self, order):
        if order:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=order.image.name)
            )


class ShipperAdmin(admin.ModelAdmin):
    class Meta:
       pass



# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Shipper,ShipperAdmin)
admin.site.register(Customer)
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(RatingShipper)

admin.site.register(Bidding)
# admin.site.register(Bidding, BiddingAdmin)
# admin.site.register(Receipt)

