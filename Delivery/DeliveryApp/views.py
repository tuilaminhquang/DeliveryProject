from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse
from django.http import HttpResponseForbidden





from .models import User, Shipper, Customer, Order, RatingShipper, Status, Comment, Bidding, Receipt
from .serializers import UserSerializers, \
    ShipperSerializers, OrderSerializers,AuthShipperSerializers,CreateShipperSerializers,\
    CreateCustomerSerializers, CustomerSerializers, CreateCommentSerializer, CommentSerializer,\
    BiddingSerializer, CreateOrderSerializers, ReceiptSerializers

# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser,]

    # def post(self, request, *args, **kwargs):
    #     username = request.data['username']
    #     password = request.data['password']
    #     email = request.data['email']
    #     first_name = request.data['first_name']
    #     last_name = request.data['last_name']
    #     avatar = request.data['avatar']
    #     User.objects.create(username=username, password=password, email=email, first_name=first_name,
    #                         last_name=last_name, avatar=avatar)
    #
    #
    #     return HttpResponse({'message': 'User created'}, status=200)
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



    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        customer = Customer.objects.get(user=request.user)
        if content:

            c = Comment.objects.create(content=content,
                                       shipper=self.get_object(),
                                       customer=customer)

            return Response(CreateCommentSerializer(c, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        shipper = self.get_object()
        comments = shipper.comments.select_related('customer').filter(active=True)

        return Response(CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


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


class CreateOrderViewSet(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = CreateOrderSerializers
    queryset = Order.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        if customer:
            serializer.save(customer=customer, status=Status.objects.get(id=1))
            # serializer.save(customer=customer)


class ShipperOrderViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = OrderSerializers
    queryset = Order.objects.filter(status=1)
    permission_classes = [permissions.IsAuthenticated]

class OrderViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    serializer_class = OrderSerializers
    queryset = Order.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]


    @action(methods=['post'], url_path='change-status', detail=True)
    def change_status(self, request, pk):
        order = self.get_object()
        order.status = Status.objects.get(pk=3)
        order.save()
        return Response(OrderSerializers(order, context={"request": request}).data,
                            status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='list-bidding', detail=True)
    def get_list(self, request, pk):
        order = self.get_object()
        customer = Customer.objects.get(user=request.user)
        if order.customer == customer:
        #if customer:
            bidding = order.bidding.select_related('shipper').all()
            return Response(BiddingSerializer(bidding, many=True, context={"request": request}).data,
                            status=status.HTTP_200_OK)
        return HttpResponseForbidden()

    @action(methods=['post'], url_path='add-receipt', detail=True)
    def add_receipt(self, request, pk):
        order = self.get_object()
        order.status = Status.objects.get(pk=2)
        order.save()
        customer = Customer.objects.get(user=request.user)
        shipper = Shipper.objects.get(pk=int(request.data.get('shipper')))
        price = request.data.get('price')
        if customer == order.customer:
            r, _= Receipt.objects.get_or_create(order=order , price=price, shipper=shipper)
        return Response(data=ReceiptSerializers(r, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)
    @action(methods=['post'], url_path='bidding', detail=True)
    def bidding(self, request, pk):
        order = self.get_object()
        shipper = Shipper.objects.get(user=request.user)

        if shipper:
            b, _ = Bidding.objects.get_or_create(shipper=shipper, order=order)
            b.bid = request.data.get('bid', 0)
        try:
            b.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=OrderSerializers(order, context={'request': request}).data,
                        status=status.HTTP_200_OK)



class CustomerViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='my-orders')
    def get_orders(self, request):
        orders = Customer.objects.get(user=request.user).orders.filter(active=True)

        # lessons = self.get_object().lessons.filter(active=True)
        # return Response(OrderSerializers.serializer_class(orders, context={'request': request}).data,
        #                     status=status.HTTP_200_OK)
        return Response(OrderSerializers(orders, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)





        return Response(data=OrderSerializers(orders, many=True, context={'request': request}).data,
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

class ReceiptApiView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializers
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='my-receipt')
    def get_receipt(self, request):
        shipper = Shipper.objects.get(user=request.user)
        receipts = shipper.receipts.filter(shipper=shipper)

        # lessons = self.get_object().lessons.filter(active=True)
        # return Response(OrderSerializers.serializer_class(orders, context={'request': request}).data,
        #                     status=status.HTTP_200_OK)
        return Response(ReceiptSerializers(receipts, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)