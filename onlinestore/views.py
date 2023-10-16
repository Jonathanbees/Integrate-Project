from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *
from django.db.models import query
import datetime as dt
from decimal import Decimal

# Processing functions

def expiring_products(products):
    next_to_expire={}
    for p in products:
        if p.expiration_date:
            days_to_expire=(p.expiration_date-dt.date.today()).days
            if days_to_expire<40:
                p.next_to_expire=[days_to_expire,int(p.purchase_price+((p.sale_price-p.purchase_price)*Decimal(0.2)))]
            else:
                p.next_to_expire=None
def admin(request):
    return redirect(reverse('admin:index'))

# Create your views here.
def index(request):
    """Listar Categorías"""
    products=Product.objects.all()
    expiration=products.order_by('expiration_date')[:3]
    expiring_products(expiration)
    featured=products.order_by('available_quantity')[:3]
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
    allcategories=Category.objects.order_by('name')
    """Fin listar categorías"""
    return render(request, 'onlinestore/index.html',{'products':featured,'categories':product_category,'allcategories':allcategories,'expiration':expiration})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    allcategories=Category.objects.order_by('name')
    expiring_products([product])
    return render(request, 'onlinestore/product_detail.html', {'product': product,'allcategories':allcategories})

def contact(request):
    allcategories=Category.objects.order_by('name')
    return render(request,'onlinestore/contact.html',{'allcategories':allcategories})
def about(request):
    allcategories=Category.objects.order_by('name')
    return render(request,'onlinestore/about.html',{'allcategories':allcategories})

def shop(request):
    products = Product.objects.order_by('name')
    #Buscador
    searchTerm = request.GET.get("searchProduct") #se recoge el input del buscador
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)

    categories = Category.objects.order_by('name')
    expiring_products(products)
    return render(request,'onlinestore/shop.html', {'products': products, 'categories':categories,'allcategories':categories})

def expiration_offers(request):
    products = Product.objects.order_by('expiration_date')
    categories = Category.objects.order_by('name')
    expiring_products(products)
    exp_prod=[]
    for p in products:
        if p.next_to_expire:
            exp_prod.append(p)
    return render(request,'onlinestore/expiration_offers.html', {'products': exp_prod, 'categories':categories})




#Función para filtrar por categorias
def category(request, category_id):
    products = Product.objects.all()
    categories = Category.objects.order_by('name')

    """Inicio filtrado por categoria"""
    category = get_object_or_404(Category, idcategory=category_id)
    if category:
        products = Product.objects.filter(category_idcategory = category)
    """Fin filtrado por categoria"""
    #Buscador
    searchTerm = request.GET.get("searchProduct") #se recoge el input del buscador
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)
    allcategories=Category.objects.order_by('name')
    expiring_products(products)
    return render(request, 'onlinestore/shop.html', { 'products': products, 'categories': categories,'allcategories':allcategories})