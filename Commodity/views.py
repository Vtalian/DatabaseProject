from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Commodity.models import Commodity
from .forms import CommodityForm
from django.http import Http404

# Create your views here.
def index(request):
    # commodity=Commodity.objects.all()
    # num=commodity.commodity_number
    # name=commodity.commodity_name
    # price=commodity.commodity_prince
    # context={'num':num, 'name':name, 'price':price}
    commodities=Commodity.objects.order_by('data')
    context={'commodities':commodities}
    return render(request, 'Commodity/index.html',context)

@login_required
def add_good(request):
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
            form.save()
            return redirect('Commodity:goods')
    
    context={'form':form}
    return render(request, 'Commodity/addgood.html',context)

@login_required
def goods(request):
    commodities=Commodity.objects.filter(owner=request.user).order_by('data')
    context={'commodities':commodities}
    return render(request, 'Commodity/goods.html',context)

@login_required
def good_details(request,number):
    commodity=Commodity.objects.get(number=cnumber)
    if request.user != commodity.owner:
        raise Http404
    else:
        context={'commodity':commodity}
        return render(request,'Commodity/gooddetails.html',context)
