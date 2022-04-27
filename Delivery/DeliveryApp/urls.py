from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='shippers', viewset=views.ShipperViewSet, basename='shipper')

urlpatterns = [
    path('', include(router.urls))

]
