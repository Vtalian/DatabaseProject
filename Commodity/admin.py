from django.contrib import admin

# Register your models here.
from Commodity.models import Commodity,ShoppingCart,Order,Message
admin.site.register(Commodity)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(Message)