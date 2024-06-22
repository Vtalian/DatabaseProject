from django.urls import path
from . import views

app_name = 'Commodity'
urlpatterns = [
    path('', views.index, name='index'),
    path('editcommodity/<uuid:id>', views.editcommodity, name='editcommodity'),
    path('addcommodity/', views.addcommodity, name='addcommodity'),
    path('details/<uuid:id>', views.details, name='details'),
    path('usercenter/<int:id>', views.usercenter, name='usercenter'),
    path('shoppingcart/<int:id>', views.shoppingcart, name='shoppingcart'),
    path('orders/<int:id>', views.orders, name='orders'),
    path('usercommodity/<int:id>', views.usercommodity, name='usercommodity'),
    path('orderdetails/<uuid:id>', views.orderdetails, name='orderdetails'),
    path('dropcommodity/<uuid:id>', views.dropcommodity, name='dropcommodity'),
    path('messages/<uuid:id>', views.messages, name='messages'),
    path('dropmessages/<int:id>', views.dropmessages, name='dropmessages'),
  
    path('buy/<uuid:id>', views.buy, name='buy'),
    path('submitorder/<uuid:id>', views.submitorder, name='submitorder'),
    path('search/', views.search, name='search'),

    path('buy/<uuid:commodity_id>', views.buy, name='buy'),
    path('submitorder/<uuid:commodity_id>', views.submitorder, name='submitorder'),
]
