from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='shippers', viewset=views.ShipperViewSet, basename='shipper')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls))

]
