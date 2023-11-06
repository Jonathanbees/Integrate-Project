from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from onlinestore.models import Buyer, Product, Cart, Category
import onlinestore.views as onlinestore_views
import purchase.views as purchase_views
def get_cart_ready(cartproduct,request):
    products = []
    subtotal = 0
    total=0
    discount=0
    total_units=0
    if cartproduct:
        if cartproduct[0]:
            for i in cartproduct:
                p = get_object_or_404(Product, pk=i.product_idproduct)
                p.subtotal = i.subtotal
                subtotal += i.subtotal
                p.product_units = i.product_units
                total_units+=p.product_units
                if p.product_units>=p.available_quantity:
                    p.exceed=True
                else:
                    p.exceed=False
                products.append(p)
            onlinestore_views.expiring_products(products,request)
            for p in products:
                if p.next_to_expire:
                    p.total=p.next_to_expire[1]*p.product_units
                    total+=p.total
                    p.discount=p.next_to_expire[2]*p.product_units
                    discount+=p.discount
                else:
                    p.total=round(p.sale_price*p.product_units)
                    total+=round(p.total)
    return (products,subtotal,total,discount,total_units)

@login_required
def add_to_cart(request, product_id):
    user_profile = get_object_or_404(Buyer,idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    if  user_profile and product:
        cart_entry = Cart.objects.filter(buyer_idbuyer=user_profile, product_idproduct=product).first()
        if cart_entry:
            if cart_entry.product_units < product.available_quantity:
                cart_entry.product_units += 1
                cart_entry.subtotal = product.sale_price * cart_entry.product_units
                cart_entry.save()
        else:
            Cart.objects.create(
                buyer_idbuyer=user_profile,
                product_idproduct=product,
                product_units=1,
                subtotal=product.sale_price
            )
        cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
        ready_cart=get_cart_ready(cartproduct,request)
        products = ready_cart[0]
        subtotal = ready_cart[1]
        total=ready_cart[2]
        discount=ready_cart[3]
        total_units=ready_cart[4]
        allcategories=Category.objects.order_by('name')
        return render(request,'detail.html', {'cart': products,'total':total,'discount':discount, 'subtotal': subtotal,'total_units':total_units, 'allcategories': allcategories,'order_units':purchase_views.order_units(request)})
@login_required
def add_to_cart_stay(request, product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    if user_profile and product:
        cart_entry = Cart.objects.filter(buyer_idbuyer=user_profile, product_idproduct=product).first()
        if cart_entry:
            if cart_entry.product_units < product.available_quantity:
                cart_entry.product_units += 1
                cart_entry.subtotal = product.sale_price * cart_entry.product_units
                cart_entry.save()
        else:
            Cart.objects.create(
                buyer_idbuyer=user_profile,
                product_idproduct=product,
                product_units=1,
                subtotal=product.sale_price
            )
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def see_cart(request):
    user_profile = get_object_or_404(Buyer,idbuyer=request.user.id)
    cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
    ready_cart=get_cart_ready(cartproduct,request)
    products = ready_cart[0]
    subtotal = ready_cart[1]
    total=ready_cart[2]
    discount=ready_cart[3]
    total_units=ready_cart[4]
    allcategories=Category.objects.order_by('name')
    return render(request,'detail.html', {'cart': products,'total':total,'discount':discount, 'subtotal': subtotal,'total_units':total_units, 'allcategories': allcategories,'order_units':purchase_views.order_units(request)})

def units_cart(request):
    #se pregunta si hay un usuario logeado
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Buyer,idbuyer=request.user.id)
        cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
        if cartproduct:
            ready_cart=get_cart_ready(cartproduct,request)
            units_cart=ready_cart[4]
            return units_cart
        else:
            return 0
    else:
        return None

@login_required
def reduce_one(request,product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    register_to_reduce=Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer, product_idproduct=product)[0]
    if register_to_reduce.product_units>1:
        register_to_reduce.product_units -= 1
        register_to_reduce.subtotal = product.sale_price * register_to_reduce.product_units
        register_to_reduce.save()
    cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
    ready_cart=get_cart_ready(cartproduct,request)
    products = ready_cart[0]
    subtotal = ready_cart[1]
    total=ready_cart[2]
    discount=ready_cart[3]
    total_units=ready_cart[4]
    return render(request,'detail.html', {'cart': products,'total':total,'discount':discount, 'subtotal': subtotal,'total_units':total_units,'order_units':purchase_views.order_units(request)})

@login_required
def delete(request, product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    register_to_delete=Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer, product_idproduct=product)
    if register_to_delete:
        r=register_to_delete.first()
        r.delete()
    cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
    ready_cart=get_cart_ready(cartproduct,request)
    products = ready_cart[0]
    subtotal = ready_cart[1]
    total=ready_cart[2]
    discount=ready_cart[3]
    total_units=ready_cart[4]
    return render(request,'detail.html', {'cart': products,'total':total,'discount':discount, 'subtotal': subtotal,'total_units':total_units,'order_units':purchase_views.order_units(request)})

@login_required
def delete_stay(request, product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    register_to_delete=Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer, product_idproduct=product)
    if register_to_delete:
        r=register_to_delete.first()
        r.delete()
    return redirect(request.META.get('HTTP_REFERER'))


