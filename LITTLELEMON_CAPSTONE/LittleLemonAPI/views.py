from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MenuItem, Category,Cart,Order,OrderItem
from .serializers import MenuItemGetSerializer, CategorySerializer,MenuItemPostSerializer,CartGetSerializer,CartPostSerializer,OrderGetSerializer,OrderPostSerializer,OrderItemPostSerializer,OrderItemGetSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.throttling import AnonRateThrottle  # for non-authenticated users
from rest_framework.throttling import UserRateThrottle  # for authenticated users
import json
from django.contrib.auth.models import User,Group
from rest_framework.permissions import IsAdminUser
import datetime

##menu_item create

@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
#@permission_classes([IsAdminUser])
def category_items(request):
    if (request.method == 'GET'):
        items = Category.objects.all()

        return_items = CategorySerializer(items, many=True)
        return Response(return_items.data)
    elif (request.method == 'POST'):

        serialized_item = CategorySerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
# @throttle_classes([AnonRateThrottle]) ##can only be used for api that does not require authentication
@permission_classes([IsAuthenticated])
def menu_items(request):
  
    if (request.method == 'GET'):
        
        items = MenuItem.objects.select_related('category').all()
        filters = {}
        for param, value in request.GET.items():
            filters[param] = value
        items = items.filter(**filters)
        
        search = request.query_params.get('search')
        # sort feature
        sort = request.query_params.get('sort')
        # pagination
        pageSize = request.query_params.get('pageSize')
        page = request.query_params.get('page')
        
        if search:
            # i is for case insensitive.contains is to see if word got the characters
            # must be double underscore even if say price__lte
            items = items.filter(Q(title__icontains=search)
                                 | Q(price__icontains=search))
        if sort:
            items = items.order_by(sort)
        if (page and pageSize):
            paginator = Paginator(items, per_page=pageSize)
            try:
                items = paginator.page(number=page)
            except EmptyPage:
                items = []
        return_items = MenuItemGetSerializer(items, many=True)
        return Response(return_items.data)
    elif (request.method == 'POST'):
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemPostSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
            return Response({"message":"Unauthorized to create new menu item"})
    
    
    

@api_view(['PUT','PATCH', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    if (request.method == 'GET'):

        return_item = MenuItemSerializer(item)
        return Response(return_item.data)
    elif (request.method == 'PUT'):
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(item, data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
            return Response({"message":"Unauthorized to do this operation"})
    elif (request.method == 'DELETE'):
        if request.user.groups.filter(name='Manager').exists():
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Unauthorized to do this operation"})


##assign to manager group
@api_view(['POST','GET'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAdminUser])
def manager(request):
    managers = Group.objects.get(name='Manager')
    if request.method == 'POST':
        if(request.data['username']):
            username=request.data['username']
            user=get_object_or_404(User,username=username)
            managers.user_set.add(user)
            return Response({"message":"User added to manager group"})
        else:
            return Response({"message":"Please choose the username to assign"})
    elif request.method == 'GET':
        _managers=managers.user_set.all()
        arr_users=[]
        for user in _managers:
           arr_users.append({'id': user.id,'username': user.username,'email': user.email})
       
        return Response(arr_users,status=status.HTTP_200_OK)
        
    return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAdminUser])
def delete_manager(request,id):
    user = get_object_or_404(User, pk=id)
    managers = Group.objects.get(name='Manager')
    if request.method == 'DELETE':
        managers.user_set.remove(user)
        return Response({"message":"User deleted from manager group"})
        
    
    return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)



##assign to delivery crew
@api_view(['POST','GET'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if request.user.groups.filter(name='Manager').exists():
        delivery_crews = Group.objects.get(name='Delivery Crew')
        if request.method == 'POST':
            if(request.data['username']):
                username=request.data['username']
                user=get_object_or_404(User,username=username)
                delivery_crews.user_set.add(user)
                return Response({"message":"User added to delivery crew group"})
            else:
                return Response({"message":"Please choose the username to assign"})
        elif request.method == 'GET':
            _delivery_crews=delivery_crews.user_set.all()
            arr_users=[]
            for user in _delivery_crews:
                arr_users.append({'id': user.id,'username': user.username,'email': user.email})
       
            return Response(arr_users,status=status.HTTP_200_OK)
        
        return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({"message":"You are not authorized to assign users to this group"})
    

@api_view(['DELETE'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def delete_delivery_crew(request,id):
    user = get_object_or_404(User, pk=id)
    delivery_crews = Group.objects.get(name='Delivery Crew')
    if request.method == 'DELETE':
        delivery_crews.user_set.remove(user)
        return Response({"message":"User deleted from delivery crew group"})
        
    
    return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)



###cart###make sure its for the particular user.make sure role is not delivery or manager


@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cart_items(request):
    manager_group=request.user.groups.filter(name='Manager').exists()
    delivery_crew_group=request.user.groups.filter(name='Delivery Crew').exists()
    
    if(manager_group==False and delivery_crew_group==False):
        if (request.method == 'GET'):
            items = Cart.objects.filter(user=request.user)
            
            return_items = CartGetSerializer(items, many=True)
            
            return Response(return_items.data)
        elif (request.method == 'POST'):
            ##req.body only need menuitem and quantity field
            menuitem= get_object_or_404(MenuItem, pk=request.data['menuitem']) ##get unitprice using the menuitem id!
            request.data['unit_price']=menuitem.price
            request.data['price']=request.data['quantity'] * menuitem.price
            request.data['user'] = request.user.id
            serialized_item = CartPostSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        elif (request.method == 'DELETE'):
            items = Cart.objects.filter(user=request.user)
            items.delete()
            return Response({"message":"Your cart items are deleted"})
    else:
        return Response({"message":"Not authorized to access cart"})


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])

def order_items(request):
    if(request.method=='POST'):
        total=0
        ##create an order record in order table.req.body no need anything since everything is from the cart
        items = Cart.objects.filter(user=request.user)
        cart_items = CartGetSerializer(items, many=True)
        data={}
        data['user']=request.user.id
        data['date']= datetime.datetime.now().date()
        for item in cart_items.data:
            total=total+float(item['price'])
        
        data['total']=total
        serialized_order = OrderPostSerializer(data=data)
        serialized_order.is_valid(raise_exception=True)
        saved_order=serialized_order.save()
        print("order record created")
        
        ##items in cart transferred to order item table
        for item in cart_items.data:
            new_order_item={}
            new_order_item['order']=saved_order.pk
            new_order_item['menuitem']=item['menuitem']['id']
            new_order_item['quantity']=item['quantity']
            new_order_item['unit_price']=item['unit_price']
            new_order_item['price']=item['price']
            serialized_order_item = OrderItemPostSerializer(data=new_order_item)
            serialized_order_item.is_valid(raise_exception=True)
            serialized_order_item.save()
        
        ##delete items in cart
        items.delete()
        return Response({"message":"Order created.You will be receiving your food shortly"})    
            
    if(request.method=='GET'):
        if(request.user.groups.filter(name='Manager').exists()):
            orders=OrderItem.objects.all()
            return_items = OrderItemGetSerializer(orders, many=True)
            
            
        else:
            if(request.user.groups.filter(name='Delivery Crew').exists()):
                orders=OrderItem.objects.filter(order__delivery_crew=request.user)
                return_items=OrderItemGetSerializer(orders,many=True)
            else:
                orders=OrderItem.objects.filter(order__user=request.user)
                return_items = OrderItemGetSerializer(orders, many=True)
            
        return Response(return_items.data)
    





@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])

def single_order_item(request,id):
    order_item = get_object_or_404(OrderItem, pk=id)
    
    if(request.method=='GET'):
        return_item = OrderItemGetSerializer(order_item)
       
        if(return_item.data['order']['user']['id']==request.user.id):
            return Response(return_item.data)
        else:
            return Response({"message":"Not authorized to see this order item"})
        