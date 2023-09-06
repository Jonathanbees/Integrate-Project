from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *

def admin(request):
    return redirect(reverse('admin:index'))

# Create your views here.
def index(request):
    products=Product.objects.all()
    featured=products.order_by('sale_price')[:3]
    categories=Category.objects.all()
    i=0
    product_category=[]
    for c in categories:
        if i<3:
            p=products.filter(category_idcategory=c.idcategory)
            if p:
                product_category.append((c,p[0]))
                i+=1
    for p in product_category:
        print(p)
    return render(request, 'onlinestore/index.html',{'products':featured,'categories':product_category})

def contact(request):
    return render(request,'onlinestore/contact.html')
def about(request):
    return render(request,'onlinestore/about.html')
def shop(request):
    searchTerm = request.GET.get('search')
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request,'onlinestore/shop.html', {'searchTerm': searchTerm, 'products': products, 'categories':categories})
