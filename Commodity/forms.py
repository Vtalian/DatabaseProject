from django import forms
from .models import Commodity

class CommodityForm(forms.ModelForm):
    
    class Meta:
        model=Commodity
        fields=['name','image','price']
        labels={'name':'商品名称','image':'商品图片','price':'商品价格'}