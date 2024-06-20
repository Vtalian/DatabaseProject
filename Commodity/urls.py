from django.urls import path
from . import views

app_name='Commodity'
urlpatterns=[
    path('',views.index,name='index'),
    path('addgoods/',views.add_good,name='addgoods'),
    path('details/<uuid:number>',views.details,name='details')
]