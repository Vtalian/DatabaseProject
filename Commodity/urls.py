from django.urls import path
from . import views

app_name='Commodity'
urlpatterns=[
    path('',views.index,name='index'),
    path('goods/',views.goods,name='goods'),
    path('addgoods/',views.add_good,name='addgoods'),
    path('gooddetails/<uuid:number>',views.good_details,name='gooddetails')
]