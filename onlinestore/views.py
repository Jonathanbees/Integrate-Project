from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *

def admin(request):
    return redirect(reverse('admin:index'))

# Create your views here.
def index(request):
    return render(request, 'onlinestore/index.html')

def contact(request):
    return render(request,'onlinestore/contact.html')
def about(request):
    return render(request,'onlinestore/about.html')
def shop(request):
    searchTerm = request.GET.get('searchProduct')
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request,'onlinestore/shop.html', {'searchTerm': searchTerm, 'products': products, 'categories':categories})
