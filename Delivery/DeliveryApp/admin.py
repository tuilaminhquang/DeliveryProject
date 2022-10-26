from django.contrib import admin
from .models import User,Order,Shipper,Customer, Status, Comment, Bidding, RatingShipper, Receipt
from django.utils.html import mark_safe
from django import forms
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, Q

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
    def get_urls(self):
        return [
                   path('shipper-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        receipt = Receipt.objects.all()
        c = receipt.count()
        stats = Shipper.objects.annotate(
            receipts_count=Count('receipts'),
            shipper_revenue=Sum('receipts__price')).values('id', 'user__first_name', 'receipts_count',
                                                           'shipper_revenue')
        stats2 = receipt \
            .values('created_date__month') \
            .annotate(sum=Sum('price')).order_by()

        if request.method == "POST" and request.POST['from_date'] and request.POST['to_date']:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            receipt = Receipt.objects.filter(created_date__range=(from_date, to_date))
            stats = Shipper.objects.annotate(
                receipts_count=Count('receipts', filter=Q(receipts__created_date__range=(from_date, to_date))),
                shipper_revenue=Sum('receipts__price', filter=Q(receipts__created_date__range=(from_date, to_date)))
            ).values('id', 'user__first_name', 'receipts_count', 'shipper_revenue')
            stats2 = receipt \
                .values('created_date__month') \
                .annotate(sum=Sum('price')).order_by()
        sum = receipt.aggregate(Sum('price'))

        return TemplateResponse(request,
                                'admin/shipper-stats.html', {
                                    'count': c,
                                    'stats': stats,
                                    'receipt': receipt,
                                    'sum': sum,
                                    'stats2': stats2,

                                })


class ReceiptAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
                   path('receipt-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):

        receipt = Receipt.objects.all()
        c = receipt.count()
        stats = Shipper.objects.annotate(
            receipts_count=Count('receipts'),
            shipper_revenue=Sum('receipts__price')).values('id', 'user__first_name','receipts_count', 'shipper_revenue')
        stats2 = receipt \
            .values('created_date__month') \
            .annotate(sum=Sum('price')).order_by()

        if request.method == "POST" and request.POST['from_date'] and request.POST['to_date']:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            receipt = Receipt.objects.filter(created_date__range=(from_date,to_date))
            stats = Shipper.objects.annotate(
                receipts_count=Count('receipts',filter=Q(receipts__created_date__range=(from_date,to_date))),
                shipper_revenue=Sum('receipts__price', filter=Q(receipts__created_date__range=(from_date,to_date)))
                ).values('id', 'user__first_name','receipts_count', 'shipper_revenue')
            stats2 = receipt\
                .values('created_date__month')\
                .annotate(sum=Sum('price')).order_by()
        sum = receipt.aggregate(Sum('price'))


        return TemplateResponse(request,
                                'admin/receipt-stats.html', {
                                    'count': c,
                                    'stats': stats,
                                    'receipt': receipt,
                                    'sum': sum,
                                    'stats2': stats2,

                                })


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
admin.site.register(Receipt, ReceiptAdmin)

