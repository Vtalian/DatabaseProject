from django.contrib import admin

# Register your models here.
from Commodity.models import *
admin.site.register(Commodity)
admin.site.register(ShoppingCart)
admin.site.register(Order)
admin.site.register(Message)
admin.site.register(Search_History)