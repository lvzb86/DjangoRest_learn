from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from computerapp.models import Product, UserProfile, DeliveryAddress, Order
from computerapp.serializer import ProductListSerializer, ProductRetrieveSerializer, UserInfoSerializer, UserProfileSerializer, UserSerializer, DeliveryAddressSerializer, OrderListSerializer, OrderCreateSerializer, OrderRUDSerializer

import logging
import datetime

LOG_FILENAME = 'shop.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
# logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

# Create your views here.


class ProductListView(generics.ListAPIView):
    """
    产品列表
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    Permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter, SearchFilter)  # 排序搜索
    ordering_fields = ('category', 'sold', 'manufacturer', 'created', )
    search_fields = ('model', )
    ordering = ('id', )
    pagination_class = LimitOffsetPagination


class ProductListByCategoryView(generics.ListAPIView):
    """
    产品
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter,)
    ordering_fields = ('category', 'sold', 'manufacturer', 'price', )
    search_fields = ('descripition', )
    ordering = ('id', )

    def get_queryset(self):
        category = self.request.query_params.get('category', None)

        if category is not None:
            queryset = Product.objects.filter(
                category=category, )
        else:
            queryset = Product.objects.all()
        return queryset


class ProductListByCategoryManufacturerView(generics.ListAPIView):
    """
    产品
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter,)
    ordering_fields = ('category', 'sold', 'manufacturer', 'price', )
    search_fields = ('descripition', )
    ordering = ('id', )

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        manufacturer = self.request.query_params.get('manufacturer', None)

        if category is not None:
            queryset = Product.objects.filter(
                category=category, manufacturer=manufacturer)
        else:
            queryset = Product.objects.all()
        return queryset


class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer


class UserInfoView(APIView):
    """
    用户信息
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        serilalizer = UserInfoSerializer(user)
        return Response(serilalizer.data)


class UserProfileRUView(generics.RetrieveUpdateAPIView):
    """
    用户其他信息
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        obj = UserProfile.objects.get(user=user)
        return obj


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class DeliveryAddressLCView(generics.ListCreateAPIView):
    """
    收货地址LC
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = DeliveryAddress.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        s = serializer.save(user=user)
        profile = user.profile_of
        profile.delivery_address = s
        profile.save()


class DeliveryAddressRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    收货地址RUD
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        # obj = DeliveryAddress.objects.get(user=user)
        try:
            obj = DeliveryAddress.objects.get(id=self.kwargs['pk'], user=user)
        except Exception as e:
            raise NotFound('not found')

        return obj


class CartListView(generics.ListAPIView):
    """
    购物车cart
    """
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status='0')
        return queryset


class OrderListView(generics.ListAPIView):
    """
    订单order
    """
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(
            user=user, status__in=['1', '2', '3', '4', ])
        return queryset


class OrderCreateView(generics.CreateAPIView):
    """
    订单创建
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')
        serializer.save(user=user, price=product.price,
                        address=self.request.user.profile_of.delivery_address, status='1', )

        logging.debug('this is debug')
        logging.info('user %d cart changed, product %d related. Time is %s.',
                     user.id, product.id, str(datetime.datetime.now()))


class OrderRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    订单修改
    """
    serializer_class = OrderRUDSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        obj = Order.objects.get(user=user, id=self.kwargs['pk'])
        return obj

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user, status='1', )
