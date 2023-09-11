from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from onlinestore.models import Buyer, Category

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', 
                      {'form':UserCreateForm})            
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    buyer = Buyer(idbuyer=user.id, email=request.POST['email'], name=request.POST['name'],username=request.POST['username'],password=request.POST['password1'],preferences={'lacteos':1.5})
                    buyer.save()
                    login(request, user)
                    return redirect('index')
                except IntegrityError:
                    return render(request, 'signupaccount.html', 
                    {'form':UserCreateForm,
                    'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'signupaccount.html', 
             {'form':UserCreateForm, 'error':'Passwords do not match'})

@login_required
def logoutaccount(request):        
    logout(request)
    return redirect('index')
@login_required
def account(request):
    user=request.user
    print("El usuario:")
    print(user)
    print(user.id)
    buyer=Buyer.objects.get(idbuyer=user.id)
    allcategories=Category.objects.order_by('name')
    return render(request, 'account.html',{'buyer':buyer,'allcategories':allcategories})

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            buyer = Buyer.objects.filter(idbuyer=user.id).first()

            if buyer is not None:
                return redirect('index')
        else:
            allcategories=Category.objects.order_by('name')
            return render(request, 'loginaccount.html', {'form': AuthenticationForm, 'error': 'Invalid username or password','allcategories':allcategories})


"""
def loginaccount(request):    
    if request.method == 'GET':
        return render(request, 'loginaccount.html', 
                      {'form':AuthenticationForm})            
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])            
    username = request.POST['username']
    password = request.POST['password']
    buyer = User.objects.filter(user__username=username).first()  # Obtiene el comprador asociado al usuario
    if buyer is not None:
        user = buyer  # Obtiene el usuario a partir del comprador
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, user)
    return redirect('index')
"""