from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='shippers', viewset=views.ShipperViewSet, basename='shipper')
router.register(prefix='customers', viewset=views.CustomerViewSet, basename='customer')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='order')
router.register(prefix='register-shipper',viewset=views.CreateShipperApiView, basename='register-shipper')
router.register(prefix='register-customer', viewset=views.CreateCustomerApiView, basename='register-customer')


urlpatterns = [
    path('', include(router.urls))

]
