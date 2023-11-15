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
import json

def expiring_products(products,request):
    next_to_expire={}
    for p in products:
        if p.expiration_date:
            days_to_expire=(p.expiration_date-dt.date.today()).days
            if days_to_expire<40:
                p.next_to_expire=[days_to_expire,int(p.purchase_price+((p.sale_price-p.purchase_price)*Decimal(0.2))),round((p.sale_price-p.purchase_price)*Decimal(0.8))]
            else:
                p.next_to_expire=None
        if request.user.is_authenticated and not request.user.is_superuser:
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
    if request.user.is_superuser:
        products=Product.objects.order_by('expiration_date') #aquí solo se va a tener en cuenta la ordenación respecto a los productos próximos a vencer
        dataproducts = []
        labelsproducts = []
        #For para mostrar la cantidad de los productos en el gráfico
        for product in products:
            labelsproducts.append(product.name)
            dataproducts.append(product.available_quantity)
        #For para mostrar los productos proximos a vencer
    
        expiring_products(products,request)
        exp_prodname=[]
        exp_prodquantity=[]
        exp_proddate=[]
        for p in products:
            if p.next_to_expire:
                exp_prodname.append(p.name)
                exp_prodquantity.append(p.available_quantity)
                exp_proddate.append(p.next_to_expire[0])
        
        #For para mostrar los productos mas vendidos
        categories = Category.objects.all()
        quantityprod=products.order_by('quantity_sold')
        productsall = Product.objects.all()
        soldproducts = []
        categoryproduct = []

        for c in categories:
            categoryproducts = Product.objects.filter(category_idcategory = c.idcategory)
            categorysold = 0
            categoryproduct.append(c.name)
            for p in categoryproducts:
                categorysold += p.quantity_sold
            soldproducts.append(categorysold)
        print(soldproducts)
        print(categoryproduct)



        #expiration=products.order_by('expiration_date')[:3]
        #expiring_products(expiration,request)
        allcategories=Category.objects.order_by('name')
        #print(dataproducts)
        #print(labelsproducts)
        #print(exp_proddate)

        order = Order.objects.filter(status = 'confirmado')
        ordersp = []
        totalsales = 0
        totalsalesdiscount = 0
        for o in order:
            productorder = ProductOrder.objects.filter(order_idorder = o.idorder) #-> Se encargará de coger la orden respecto a la orden confirmada
            for p in productorder:
                totalsales += p.quantity*p.discounted_unit_price
                if p.discounted_unit_price != p.nondiscounted_unit_price:
                    totalsalesdiscount += p.quantity*p.discounted_unit_price
        print(totalsales)
        print(totalsalesdiscount)
        
        #print(order)
        #1. Filtrar por orden de acuerdo al status = confirmado
        #2. asociar orden con product-order respecto al id (categoryproducts = Product.objects.filter(category_idcategory = c.idcategory))
        #3. si el descuento es 0, no se coge el dato, per
        #ventas totales (quantity x discounted-unitprice)
        #cuanto se vendió de productos proximos a perderse (quantity x discounted-unitprice) -> que discounted_unit_pri != nondiscounted
                                                                                                #(nuevo subtotal) quantity* discounted


        return render(request, 'onlinestore/graphics.html',{
                                                            'totalsales': totalsales,
                                                            'totalsalesdiscount':totalsalesdiscount,
                                                            })

    else:
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
"""
def graphics(request):
    products=Product.objects.order_by('expiration_date') #aquí solo se va a tener en cuenta la ordenación respecto a los productos próximos a vencer
    dataproducts = []
    labelsproducts = []
    #For para mostrar la cantidad de los productos en el gráfico
    for product in products:
        labelsproducts.append(product.name)
        dataproducts.append(product.available_quantity)
    #For para mostrar los productos proximos a vencer
    
    expiring_products(products,request)
    exp_prodname=[]
    exp_prodquantity=[]
    exp_proddate=[]
    for p in products:
        if p.next_to_expire:
            exp_prodname.append(p.name)
            exp_prodquantity.append(p.available_quantity)
            exp_proddate.append(p.next_to_expire[0])
    
    #For para mostrar los productos mas vendidos
    categories = Category.objects.all()
    quantityprod=products.order_by('quantity_sold')
    productsall = Product.objects.all()
    soldproducts = []
    categoryproduct = []

    #for p in productsall:
     #   if p.category_idcategory == categories.idcategory:



    #expiration=products.order_by('expiration_date')[:3]
    #expiring_products(expiration,request)
    allcategories=Category.objects.order_by('name')
    print(dataproducts)
    print(labelsproducts)
    print(exp_proddate)


    return render(request, 'onlinestore/graphics.html',{'categories': allcategories, 'products': products, 
                                                        'labelsproducts': json.dumps(labelsproducts),
                                                        'dataproducts': dataproducts,
                                                        'exp_prodname':exp_prodname,
                                                        'exp_prodquantity': exp_prodquantity,
                                                        'exp_proddate': exp_proddate,
                                                        })
"""