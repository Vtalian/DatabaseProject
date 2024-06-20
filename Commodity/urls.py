from django.urls import path
from . import views

app_name='Commodity'
urlpatterns=[
    path('',views.index,name='index'),
    # path('editcommodity/<uuid:number>',views.editcommodity,name='editcommodity'),
    path('addcommodity/',views.addcommodity,name='addcommodity'),
    path('details/<uuid:id>',views.details,name='details')
]