from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser



from .models import User, Shipper, Customer, Order, RatingShipper, Status
from .serializers import UserSerializers, \
    ShipperSerializers, OrderSerializers,AuthShipperSerializers,CreateShipperSerializers,\
    CreateCustomerSerializers, CustomerSerializers

# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser,]

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)



class ShipperDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializers



class ShipperViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializers
    permission_classes = [permissions.IsAuthenticated]




    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        shipper = self.get_object()
        customer = Customer.objects.get(user=request.user)

        if customer:
            r, _ = RatingShipper.objects.get_or_create(shipper=shipper, customer=customer)
            r.rate = request.data.get('rate', 0)
        try:
            r.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=ShipperSerializers(shipper, context={'request': request}).data,
                        status=status.HTTP_200_OK)




class OrderViewSet(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = OrderSerializers
    queryset = Order.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)

        if customer:
            serializer.save(customer=customer, status=Status.objects.get(id=1))


class CustomerViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='orders')
    def get_orders(self, request, pk):
        orders = Customer.objects.get(pk=pk).orders.filter(active=True)
        # lessons = self.get_object().lessons.filter(active=True)


        return Response(OrderSerializers(orders, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)


class CreateCustomerApiView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = CreateCustomerSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateShipperApiView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = CreateShipperSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
