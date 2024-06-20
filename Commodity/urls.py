from django.urls import path
from . import views

app_name='Commodity'
urlpatterns=[
    path('',views.index,name='index'),
    path('editcommodity/<uuid:id>',views.editcommodity,name='editcommodity'),
    path('addcommodity/',views.addcommodity,name='addcommodity'),
    path('details/<uuid:id>',views.details,name='details'),
    path('usercenter/<int:id>',views.usercenter,name='usercenter'),
    path('shoppingcart/<int:id>',views.shoppingcart,name='shoppingcart'),
    path('orders/<int:id>',views.orders,name='orders'),
    path('usercommodity/<int:id>',views.usercommodity,name='usercommodity'),
]