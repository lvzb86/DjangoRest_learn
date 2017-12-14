from rest_framework import serializers
from django.contrib.auth.models import User

from computerapp.models import Product, Manufacturer, Category, UserProfile, DeliveryAddress, Order


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'mobile_phone', 'nickname',
                  'description', 'icon', 'created', 'updated', )
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user


class DeliveryAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ('id', 'user', 'contact_person', 'contact_mobile_phone',
                  'delivery_address', 'created', 'updated', )


class UserInfoSerializer(serializers.ModelSerializer):

    profile_of = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'date_joined', 'profile_of', )


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'model', 'image', 'price', 'sold',
                  'category', 'manufacturer', )


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ('id', 'name', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', )


class ProductRetrieveSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'model', 'image', 'price', 'sold',
                  'category', 'manufacturer', 'description', 'created', 'updated', )


class OrderListSerializer(serializers.ModelSerializer):

    product = ProductListSerializer()
    address = DeliveryAddressSerializer()

    class Meta:
        model = Order
        fields = ('status', 'user', 'remark', 'product', 'price',
                  'quantity', 'address', 'created', 'updated',)


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('status', 'user', 'remark', 'product', 'price',
                  'quantity', 'address', 'created', 'updated',)
        read_only_fields = ('user', 'price', 'address', 'status', )


class OrderRUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('status', 'user', 'remark', 'product', 'price',
                  'quantity', 'address', 'created', 'updated',)
        read_only_fields = ('user', 'price', 'address', 'status', )
