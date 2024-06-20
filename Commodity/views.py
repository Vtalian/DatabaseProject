from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Commodity.models import Commodity,ShoppingCart,Message,Order
from .forms import CommodityForm
from django.db import models
from django.conf import settings
from django.http import Http404
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
    context={'commodity':commodity,'message':message,'belong':belong}
    return render(request,'Commodity/details.html',context)

def editcommodity(request,id):
    commodity=Commodity.objects.get(id=id)
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
    shoppingcart=ShoppingCart.objects.filter(adduser=id).order_by('date')
    content={'shopingcart':shoppingcart,'type':shoppingcart}
    return render(request,'Commodity/usercenter.html',content)

def shoppingcart(request,id):#个人中心-购物车
    shoppingcart=ShoppingCart.objects.filter(adduser=id).values('commodity')
    commodity=Commodity.objects.all()

    q=models.Q()
    q.connector='OR'
    for s in shoppingcart:
        q.children.append(('id',s['commodity']))

    c=commodity.filter(q).order_by('date')
    content={'commodity':c,'type':shoppingcart}
    return render(request,'Commodity/shoppingcart.html',content)

def orders(request,id):#个人中心-订单
    orders=Order.objects.filter(purchaser=id).order_by('date')
    content={'orders':orders}
    return render(request,'Commodity/userorder.html',content)

def usercommodity(request,id):#个人中心-在售商品
    comodity=Commodity.objects.filter(owner=id,public=True,selltag=False).order_by('date')
    content={'commodity':comodity,'type':comodity}
    return render(request,'Commodity/usercenter.html',content)