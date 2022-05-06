from rest_framework import serializers
from .models import User, Shipper, Customer, Order


class UserSerializers(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')

    def get_avatar(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
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
        fields = ['user','identity_number']




class OrderSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    def get_image(self, obj):
        request = self.context['request']
        # if obj.image and obj.image.name.startswith("/static"):
        #     pass
        # else:
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)



    class Meta:
        model = Order
        fields = ['id', 'order_name', 'created_date', 'updated_date', 'shipping_method','note', 'image', 'customer']








