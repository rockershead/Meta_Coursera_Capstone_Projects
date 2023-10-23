from rest_framework import serializers
from .models import MenuItem, Category,Cart,Order,OrderItem
from decimal import Decimal
from django.contrib.auth.models import User


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","slug","title"]


class MenuItemGetSerializer(serializers.ModelSerializer):
    
    
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured','category']
class MenuItemPostSerializer(serializers.ModelSerializer):
    
    category = serializers.PrimaryKeyRelatedField( read_only=False,queryset=Category.objects.all())
   
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured','category']
        
class CartGetSerializer(serializers.ModelSerializer):
    
    
    menuitem = MenuItemGetSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'unit_price', 'price','menuitem','user']
class CartPostSerializer(serializers.ModelSerializer):
    
    
    menuitem = serializers.PrimaryKeyRelatedField( read_only=False,queryset=MenuItem.objects.all())
    user = serializers.PrimaryKeyRelatedField( read_only=False,queryset=User.objects.all())
   
    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'unit_price', 'price','menuitem','user']
        
        
        

class OrderGetSerializer(serializers.ModelSerializer):
    
    
    delivery_crew = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status','total','date']
        
class OrderPostSerializer(serializers.ModelSerializer):
    
    
    #delivery_crew = serializers.PrimaryKeyRelatedField( read_only=False,queryset=User.objects.all())
    user = serializers.PrimaryKeyRelatedField( read_only=False,queryset=User.objects.all())
   
    class Meta:
        model = Order
        fields = ['id', 'user', 'status','total','date']







class OrderItemGetSerializer(serializers.ModelSerializer):
    
    
    menuitem = MenuItemGetSerializer(read_only=True)
    order = OrderGetSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'price','menuitem','order']
        
class OrderItemPostSerializer(serializers.ModelSerializer):
    
    
    menuitem = serializers.PrimaryKeyRelatedField( read_only=False,queryset=MenuItem.objects.all())
    order = serializers.PrimaryKeyRelatedField( read_only=False,queryset=Order.objects.all())
   
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'price','menuitem','order']
        
    
        


       
