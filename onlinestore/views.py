from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *
from django.db.models import query

def admin(request):
    return redirect(reverse('admin:index'))

# Create your views here.
def index(request):
    """Listar Categorías"""
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
    """Fin listar categorías"""
    return render(request, 'onlinestore/index.html',{'products':featured,'categories':product_category})

def contact(request):
    return render(request,'onlinestore/contact.html')
def about(request):
    return render(request,'onlinestore/about.html')
def shop(request):
    products = Product.objects.all()
    #Buscador
    searchTerm = request.GET.get("searchProduct") #se recoge el input del buscador
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)

    categories = Category.objects.all()
    return render(request,'onlinestore/shop.html', {'products': products, 'categories':categories})


#Función para filtrar por categorias
def category(request, category_id):
    products = Product.objects.all()
    categories = Category.objects.all()
    """Inicio filtrado por categoria"""
    category = get_object_or_404(Category, idcategory=category_id)
    if category:
        products = Product.objects.filter(category_idcategory = category)
    """Fin filtrado por categoria"""
    #Buscador
    searchTerm = request.GET.get("searchProduct") #se recoge el input del buscador
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)
    return render(request, 'onlinestore/category.html', {'category': category, 'products': products, 'categories': categories})