from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Commodity.models import Commodity,ShoppingCart,Message,Order
from .forms import CommodityForm
from django.http import Http404

# Create your views here.
def index(request):
    commodities=Commodity.objects.filter(public=True).order_by('date')
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
def details(request,number):
    commodity=Commodity.objects.get(id=number)
    context={'commodity':commodity}
    return render(request,'Commodity/details.html',context)
