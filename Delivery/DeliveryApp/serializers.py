from rest_framework import serializers
from .models import User, Shipper, Customer, Order, Comment, Bidding
from rest_framework.fields import CurrentUserDefault



class UserSerializers(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField()

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)


    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar','avatar_path']
        extra_kwargs = {
            'password': {
                'write_only': True
            },' avatar_path': {
                'read_only':True
             , 'avatar': {
                    'write_only':True
                }
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user


class ShipperSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    class Meta:
        model = Shipper
        fields = ['id','user','identity_number']

class CustomerSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    class Meta:
        model = Customer
        fields = ['id','user','phone']

class CreateCustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone']

class CreateShipperSerializers(serializers.ModelSerializer):

    class Meta:
        model = Shipper
        fields = ['identity_number']


class AuthShipperSerializers(ShipperSerializers):
    rating = serializers.SerializerMethodField()

    def get_rating(self, shipper):
        request = self.context.get('request')
        customer = Customer.objects.get(user=request.user)
        if request:
            r = shipper.rating_set.filter(customer=customer).first()
            if r:
                return r.rate
    class Meta:
        model = Shipper
        fields = ShipperSerializers.Meta.fields + ['rating']



class OrderSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    #bidding = serializers.SerializerMethodField()

    # def get_bidding(self, order):
    #     request = self.context.get('request')
    #     customer = Customer.objects.get(user=request.user)
    #     order = Order.objects.get(customer=customer)
    #     if request:
    #         b = order.bidding_set.filter(order=customer.orders)
    #         if b:
    #             return b.rate

    def get_image(self, obj):
        request = self.context['request']
        # if obj.image and obj.image.name.startswith("/static"):
        #     pass
        # else:
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)



    class Meta:
        model = Order
        fields = ['id', 'order_name', 'created_date', 'updated_date','note',
                  'image', 'customer','km','from_address','to_address']


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content', 'shipper']

class CommentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializers()
    class Meta:
        model = Comment
        exclude = ['active']


class BiddingSerializer(serializers.ModelSerializer):
    shipper = ShipperSerializers()
    order = OrderSerializers()

    class Meta:
        model = Bidding
        fields = ["id", "bid", "created_date","shipper","order"]

