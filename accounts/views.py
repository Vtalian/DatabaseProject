from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from  Commodity.models import Search_History
# Create your views here.

def register(request):
    if request.method != 'POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user=form.save()
            Search_History(id=new_user,str="").save()
            login(request,new_user)
            return redirect('Commodity:index')
    context={'form':form}
    return render(request,'registration/register.html',context)