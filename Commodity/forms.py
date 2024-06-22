from django import forms
from .models import Commodity, Message, Order


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ['name', 'image', 'price', 'details']
        labels = {'name': '商品名称', 'image': '商品图片', 'price': '商品价格', 'details': '详情'}
        widgets = {'details': forms.Textarea(attrs={'col': 80})}


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {'content': '发表留言吧！'}
        widgets = {'content': forms.Textarea(attrs={'class': "form-control", 'col': 10, 'row': 2})}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['remark']
        labels = {'remark': '添加备注'}
        widgets = {'details': forms.Textarea(attrs={'col': 80})}
