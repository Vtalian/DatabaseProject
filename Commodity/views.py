from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Commodity.models import *
from .forms import CommodityForm, MessageForm, OrderForm
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.http import Http404
from utils.paging import Paging
import os


# 用户验证
def user_confirm(request, user):
    if request.user != user:
        raise Http404


# Create your views here.
def index(request, page=1):
    commodities = Commodity.objects.filter(public=True, selltag=False).order_by('date')
    # context={'commodities':commodities}
    page = Paging(request, lengths=commodities.count(), page_num=5, max_page_num=9)
    return render(request, 'Commodity/index.html',
                  {'commodities': commodities[page.start:page.end], 'html_list': page.html_list})
    # return render(request, 'Commodity/index.html',context)


@login_required
def addcommodity(request):
    if request.method != 'POST':
        form = CommodityForm()
    else:
        form = CommodityForm(request.POST, request.FILES)
        if form.is_valid():
            # new_name=getNewName(form.cleaned_data['commodity_name'])
            # where='%s/Commodity/%s'%(settings.MEDIA_ROOT,new_name)

            # with open(where,'wb+') as destination:
            #     for i in request.FILES['image'].chunks():
            #         destination.write(i)
            # form.cleaned_data['image']=new_name
            c = form.save(commit=False)
            c.owner = request.user
            id = c.id
            c.save()
            return redirect('Commodity:details', id=id)

    context = {'form': form}
    return render(request, 'Commodity/addcommodity.html', context)


@login_required
def details(request, id):
    commodity = Commodity.objects.get(id=id)
    message = Message.objects.filter(name=id).order_by('date')
    if request.user == commodity.owner:
        belong = True
    else:
        belong = False
    form = MessageForm()
    context = {'commodity': commodity, 'messages': message, 'belong': belong, 'form': form, 'user': request.user}
    return render(request, 'Commodity/details.html', context)


@login_required
def editcommodity(request, id):
    commodity = Commodity.objects.get(id=id)
    user_confirm(request, commodity.owner)
    prename = commodity.image
    if request.method != 'POST':
        form = CommodityForm(instance=commodity)
    else:
        form = CommodityForm(request.POST, request.FILES, instance=commodity)
        if form.is_valid():
            form.save()
            nowcommodity = Commodity.objects.get(id=id)
            if prename != nowcommodity.image:
                path = '%s/%s' % (settings.MEDIA_ROOT, prename)
                os.remove(path)
            return redirect('Commodity:details', id=id)

    content = {'commodity': commodity, 'form': form}
    return render(request, 'Commodity/editcommodity.html', content)


def usercenter(request, id):  # 个人中心主页，默认展示购物车
    user_confirm(request, User.objects.get(id=id))
    shoppingcart = ShoppingCart.objects.filter(adduser=id).values('commodity')
    if shoppingcart.count() == 0:
        content = {'commodity': shoppingcart}
    else:
        commodity = Commodity.objects.all()

        q = models.Q()
        q.connector = 'OR'
        for s in shoppingcart:
            q.children.append(('id', s['commodity']))

        c = commodity.filter(q).order_by('date')
        content = {'commodity': c}
    return render(request, 'Commodity/usercenter.html', content)


def shoppingcart(request, id):  # 个人中心-购物车
    user_confirm(request, User.objects.get(id=id))
    shoppingcart = ShoppingCart.objects.filter(adduser=id).values('commodity')
    if shoppingcart.count() == 0:
        content = {'commodity': shoppingcart}
    else:
        commodity = Commodity.objects.all()

        q = models.Q()
        q.connector = 'OR'
        for s in shoppingcart:
            q.children.append(('id', s['commodity']))

        c = commodity.filter(q).order_by('date')
        content = {'commodity': c}
    return render(request, 'Commodity/shoppingcart.html', content)


def orders(request, id):  # 个人中心-订单
    user = User.objects.get(id=id)
    user_confirm(request, user)
    q = models.Q()
    q.connector = 'OR'
    q.children.append(('purchaser', user))
    q.children.append(('seller', user))
    orders = Order.objects.filter(q).order_by('date')
    content = {'orders': orders}
    return render(request, 'Commodity/userorder.html', content)


def usercommodity(request, id):  # 个人中心-在售商品
    user = User.objects.get(id=id)
    user_confirm(request, user)
    comodity = Commodity.objects.filter(owner=id, public=True, selltag=False).order_by('date')
    content = {'commodity': comodity, 'type': comodity}
    return render(request, 'Commodity/usercommodity.html', content)


def dropcommodity(request, id):
    if request.method == 'POST':
        commodity = Commodity.objects.get(id=id)
        name = commodity.image
        path = '%s/%s' % (settings.MEDIA_ROOT, name)
        commodity.delete()
        os.remove(path)
        return redirect('Commodity:index')


def messages(request, id):
    if request.method != 'POST':
        form = MessageForm()
    else:
        commodity = Commodity.objects.get(id=id)
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.name = commodity
            message.speaker = request.user
            message.save()
            return redirect('Commodity:details', id)
        else:
            raise Http404


def dropmessages(request, id):
    message = Message.objects.get(id=id)
    if request.method == 'POST' and request.user == message.speaker:
        message.delete()
        return redirect('Commodity:details', message.name.id)


def buy(request, commodity_id):
    if request.method != 'POST':
        commodity = Commodity.objects.get(id=commodity_id)
        form = OrderForm()
        content = {'commodity': commodity, 'form': form}

        return render(request, 'Commodity/buy.html', content)
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)

            commodity = Commodity.objects.get(id=commodity_id)
            f.commodity_id = commodity
            f.purchaser = request.user
            f.seller = commodity.owner
            f.save()
            return redirect('Commodity:orderdetails', orderid)


def submitorder(request, commodity_id):
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid:
            f = form.save(commit=False)
            orderid = f.orderid
            commodity = Commodity.objects.get(id=commodity_id)
            f.commodity_id = commodity
            f.purchaser = request.user
            f.seller = commodity.owner
            f.save()
            commodity.selltag = True
            commodity.save()

            ShoppingCart.objects.get(commodity=commodity, adduser=request.user).delete()
            return redirect('Commodity:orderdetails', orderid)


def orderdetails(request, id):
    order = Order.objects.get(orderid=id)
    commodity = order.commodity_id
    if order.senttag == False:
        tag = '未发货'
        color = 1
    elif order.senttag and order.receipttag == False:
        tag = '未收货'
        color = 2
    else:
        tag = '已完成'
        color = 3
    content = {'order': order, 'commodity': commodity, 'tag': tag, 'color': color}
    return render(request, 'Commodity/orderdetails.html', content)


def search(request):
    his = Search_History.objects.get(id=request.user)
    message = his.str
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['content']
            his.str = message
            his.save()
    commodities = Commodity.objects.filter(public=True, selltag=False, name__contains=message).order_by('date')
    if commodities.count() > 5:
        tag = True
    else:
        tag = False
    page = Paging(request, lengths=commodities.count(), page_num=5, max_page_num=9)
    return render(request, 'Commodity/search.html',
                  {'commodities': commodities[page.start:page.end], 'html_list': page.html_list, 'tag': tag})
