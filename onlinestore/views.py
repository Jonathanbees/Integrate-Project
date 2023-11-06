from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *
from django.db.models import query
import datetime as dt
from decimal import Decimal
import cart.views as cart_views
from purchase import views as purchase_views

def expiring_products(products,request):
    next_to_expire={}
    for p in products:
        if p.expiration_date:
            days_to_expire=(p.expiration_date-dt.date.today()).days
            if days_to_expire<40:
                p.next_to_expire=[days_to_expire,int(p.purchase_price+((p.sale_price-p.purchase_price)*Decimal(0.2))),round((p.sale_price-p.purchase_price)*Decimal(0.8))]
            else:
                p.next_to_expire=None
        if request.user.is_authenticated:
            buyer =get_object_or_404(Buyer,idbuyer=request.user.id)
            in_cart=Cart.objects.filter(buyer_idbuyer=buyer,product_idproduct=p)
            if in_cart:
                p.in_cart=True
            in_wishlist=Wishlist.objects.filter(buyer_idbuyer=buyer,product_idproduct=p)
            if in_wishlist:
                p.in_wishlist=True
def admin(request):
    return redirect(reverse('admin:index'))

def index(request):
    products=Product.objects.filter(available_quantity__gt=0)
    expiration=products.order_by('expiration_date')[:3]
    expiring_products(expiration,request)
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
    allcategories=Category.objects.order_by('name')
    total_units=cart_views.units_cart(request)
    purchase_views.release_stock()
    return render(request, 'onlinestore/index.html',{'total_units':total_units,'products':featured,'categories':product_category,'allcategories':allcategories,'expiration':expiration,'order_units':purchase_views.order_units(request)})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    allcategories=Category.objects.order_by('name')
    expiring_products([product],request)
    total_units=cart_views.units_cart(request)
    if request.user.is_authenticated:
        product.purchased=purchase_views.purchased_product(request,product_id)
    return render(request, 'onlinestore/product_detail.html', {'total_units':total_units,'product': product,'allcategories':allcategories,'order_units':purchase_views.order_units(request)})

def contact(request):
    allcategories=Category.objects.order_by('name')
    return render(request,'onlinestore/contact.html',{'allcategories':allcategories,'order_units':purchase_views.order_units(request)})
def about(request):
    allcategories=Category.objects.order_by('name')
    return render(request,'onlinestore/about.html',{'allcategories':allcategories,'order_units':purchase_views.order_units(request)})

def shop(request):
    products = Product.objects.filter(available_quantity__gt=0).order_by('name')
    searchTerm = request.GET.get("searchProduct")
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)

    categories = Category.objects.order_by('name')
    expiring_products(products,request)
    total_units=cart_views.units_cart(request)
    purchase_views.release_stock()
    return render(request,'onlinestore/shop.html', {'total_units':total_units,'products': products, 'categories':categories,'allcategories':categories,'order_units':purchase_views.order_units(request)})

def expiration_offers(request):
    products = Product.objects.order_by('expiration_date')
    categories = Category.objects.order_by('name')
    expiring_products(products,request)
    exp_prod=[]
    for p in products:
        if p.next_to_expire:
            exp_prod.append(p)
    total_units=cart_views.units_cart(request)
    purchase_views.release_stock()
    return render(request,'onlinestore/expiration_offers.html', {'total_units':total_units,'products': exp_prod, 'categories':categories, 'allcategories': categories,'order_units':purchase_views.order_units(request)})

def category(request, category_id):
    products = Product.objects.all()
    categories = Category.objects.order_by('name')
    category = get_object_or_404(Category, idcategory=category_id)
    if category:
        products = Product.objects.filter(category_idcategory = category,available_quantity__gt=0)
    searchTerm = request.GET.get("searchProduct")
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)
    allcategories=Category.objects.order_by('name')
    expiring_products(products,request)
    total_units=cart_views.units_cart(request)
    purchase_views.release_stock()
    return render(request, 'onlinestore/shop.html', {'total_units':total_units, 'products': products, 'categories': categories,'allcategories':allcategories,'order_units':purchase_views.order_units(request)})