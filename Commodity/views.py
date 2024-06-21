from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Commodity.models import Commodity,ShoppingCart,Message,Order
from .forms import CommodityForm,MessageForm,OrderForm
from django.db import models
from django.conf import settings
from django.http import Http404
from django.contrib import messages
from utils import methods
import os

# Create your views here.
def index(request):
    commodities=Commodity.objects.filter(public=True).order_by('date')
    context={'commodities':commodities}
    return render(request, 'Commodity/index.html',context)

@login_required
def addcommodity(request):
    if request.method != 'POST':
        form=CommodityForm()
    else:
        form=CommodityForm(request.POST,request.FILES)
        if form.is_valid():
            # new_name=getNewName(form.cleaned_data['commodity_name'])
            # where='%s/Commodity/%s'%(settings.MEDIA_ROOT,new_name)

            # with open(where,'wb+') as destination:
            #     for i in request.FILES['image'].chunks():
            #         destination.write(i)
            # form.cleaned_data['image']=new_name
            c=form.save(commit=False)
            c.owner=request.user
            id=c.id
            c.save()
            return redirect('Commodity:details',id=id)
    
    context={'form':form}
    return render(request, 'Commodity/addcommodity.html',context)

@login_required
def goods(request):
    commodities=Commodity.objects.filter(owner=request.user).order_by('date')
    context={'commodities':commodities}
    return render(request, 'Commodity/goods.html',context)


def details(request,id):
    commodity=Commodity.objects.get(id=id)
    message=Message.objects.filter(name=id).order_by('date')
    if request.user==commodity.owner:
        belong=True
    else:
        belong=False
    form=MessageForm()
    context={'commodity':commodity,'messages':message,'belong':belong,'form':form,'user':request.user}
    return render(request,'Commodity/details.html',context)

def editcommodity(request,id):
    commodity=Commodity.objects.get(id=id)
    if request.user != commodity.owner:
        raise Http404
    prename=commodity.image
    if request.method != 'POST':
        form=CommodityForm(instance=commodity)
    else:
        form=CommodityForm(request.POST,request.FILES,instance=commodity)
        if form.is_valid():
            form.save()
            nowcommodity=Commodity.objects.get(id=id)
            if prename!=nowcommodity.image:
                path='%s/%s' %(settings.MEDIA_ROOT,prename)
                os.remove(path)
            return redirect('Commodity:details',id=id)
    
    content={'commodity':commodity,'form':form}
    return render(request,'Commodity/editcommodity.html',content)

def usercenter(request,id):#个人中心主页，默认展示购物车
    shoppingcart=ShoppingCart.objects.filter(adduser=id).values('commodity')
    commodity=Commodity.objects.all()

    q=models.Q()
    q.connector='OR'
    for s in shoppingcart:
        q.children.append(('id',s['commodity']))

    c=commodity.filter(q).order_by('date')
    content={'commodity':c}
    return render(request,'Commodity/usercenter.html',content)

def shoppingcart(request,id):#个人中心-购物车
    shoppingcart=ShoppingCart.objects.filter(adduser=id).values('commodity')
    commodity=Commodity.objects.all()

    q=models.Q()
    q.connector='OR'
    for s in shoppingcart:
        q.children.append(('id',s['commodity']))

    c=commodity.filter(q).order_by('date')
    content={'commodity':c}
    return render(request,'Commodity/shoppingcart.html',content)

def orders(request,id):#个人中心-订单
    orders=Order.objects.filter(purchaser=id).order_by('date')
    p=Order.objects.filter(purchaser=id).order_by('date')
    p=p.values('commodity_id')

    q=models.Q()
    q.connector='OR'
    for ps in p:
        q.children.append(('id',ps['commodity_id']))

    commodity=Commodity.objects.all().filter(q).order_by('date')
    content={'orders':orders,'commodity':commodity}
    return render(request,'Commodity/userorder.html',content)

def usercommodity(request,id):#个人中心-在售商品
    if request.user == id:
        raise Http404
    comodity=Commodity.objects.filter(owner=id,public=True,selltag=False).order_by('date')
    content={'commodity':comodity,'type':comodity}
    return render(request,'Commodity/usercenter.html',content)

def orderdetails(request,id):
    return render(request,'Order/orderdetails.html')

def dropcommodity(request,id):
    if request.method == 'POST':
        commodity=Commodity.objects.get(id=id)
        name=commodity.image
        path='%s/%s' %(settings.MEDIA_ROOT,name)
        commodity.delete()
        os.remove(path)
        return redirect('Commodity:index')

def messages(request,id):
    if request.method != 'POST':
        form=MessageForm()
    else:
        commodity=Commodity.objects.get(id=id)
        form=MessageForm(data=request.POST)
        message=form.save(commit=False)
        message.name=commodity
        message.speaker=request.user
        message.save()
        return redirect('Commodity:details',id)
    
def dropmessages(request,id):
    message=Message.objects.get(id=id)
    if request.method=='POST' and request.user == message.speaker:
        message.delete()
        messages.success(request,'删除成功')
        return redirect('Commodity:details',message.name.id)
    
def buy(request,id):
    commodity=Commodity.objects.get(id=id)
    form=OrderForm()
    content={'commodity':commodity,'form':form}
    return render(request,'Commodity/buy.html',content)

def submitorder(request,id):
    if request.method == 'POST':
        form=OrderForm(data=request.POST)
        if form.is_valid:
            order=form.save(commit=False)
            c=Commodity.objects.get(id=id)
            order.commodity_id=c
            order.purchaser=request.user
            order.save()
            ShoppingCart.objects.get(commodity=c,adduser=request.user).delete()
            return redirect('Commodity:shoppingcart',request.user.id)