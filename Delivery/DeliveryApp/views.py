from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Shipper, Customer
from .serializers import UserSerializers, ShipperSerializers

# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)

class ShipperViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializers
