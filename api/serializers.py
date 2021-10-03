from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category_id')


class SubcategorySerializerGet(serializers.ModelSerializer):
    category = serializers.CharField(source='category_id.name')

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category_id', 'category')


class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = ('id', 'name', 'value', 'type_value')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'description', 'is_active', 'cost', 'profit', 'subcategory_id',
                  'photo_file_name', 'photo_file_name2', 'photo_file_name3', 'expenses', 'highlight', 'on_sale')
        depth = 1


class ProductSerializerGet(serializers.ModelSerializer):
    category = serializers.CharField(source='subcategory_id.category_id.name')
    subcategory = serializers.CharField(source='subcategory_id.name')

    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'description', 'is_active', 'cost', 'profit', 'subcategory_id',
                  'photo_file_name', 'photo_file_name2', 'photo_file_name3', 'subcategory', 'category', 'expenses',
                  'highlight', 'on_sale')


class StockSerializerGet(serializers.ModelSerializer):
    product = serializers.CharField(source='product_id.name')

    class Meta:
        model = Stock
        fields = ('id', 'name', 'amount', 'product_id', 'product')


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('id', 'name', 'amount', 'product_id')


class SellSerializerGet(serializers.ModelSerializer):

    def getUsername(self, obj):
        return obj.user.username

    username = serializers.SerializerMethodField("getUsername")
    product = serializers.CharField(source='product_id.name')


    class Meta:
        model = Sell
        fields = ('id', 'date', 'pending', 'shipping', 'total', 'client', 'product_id')


class SellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sell
        fields = ('id', 'shipping', 'total', 'client', 'product_id')


class ClientDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientData
        fields = ('id', 'first_name', 'last_name', 'address', 'province', 'city', 'neighborhood', 'cp',
                  'phone', 'user_id')



