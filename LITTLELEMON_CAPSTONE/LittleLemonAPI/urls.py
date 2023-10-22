from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('categories', views.category_items),
    path('menu-items', views.menu_items),
    path('menu-items/<int:id>', views.single_item),
    path('groups/manager/users',views.manager),
    path('groups/manager/users/<int:id>',views.delete_manager),
    path('groups/delivery-crew/users',views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>',views.delete_delivery_crew),
    path('cart/menu-items',views.cart_items)
    
    

]
