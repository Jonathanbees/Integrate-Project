from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from onlinestore.models import Buyer, Product, Wishlist, Cart, Category
import onlinestore.views as onlinestore_views
import cart.views as cart_views


@login_required
def add_to_wishlist(request, product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    if user_profile and product:
        wishlist_entry = Wishlist.objects.filter(product_idproduct=product,buyer_idbuyer=user_profile).first()
        if wishlist_entry:
            pass
        else:
            Wishlist.objects.create(
                product_idproduct=product,
                buyer_idbuyer=user_profile,
                )
        return redirect(request.META.get('HTTP_REFERER'))
    
@login_required
def ver_wishlist(request):
    user_profile = get_object_or_404(Buyer,idbuyer=request.user.id)
    wishlist= Wishlist.objects.all().filter(buyer_idbuyer=user_profile)
    products=[]
    for i in wishlist:
            p = get_object_or_404(Product, pk=i.product_idproduct)
            products.append(p)
    onlinestore_views.expiring_products(products,request)
    total_units=cart_views.units_cart(request)
    allcategories=Category.objects.order_by('name')
    return render(request,'wishlist.html', {'wishlist': products, 'total_units':total_units, 'allcategories':allcategories })

@login_required
def delete_stay(request, product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    register_to_delete=Wishlist.objects.all().filter(buyer_idbuyer=user_profile.idbuyer, product_idproduct=product)
    if register_to_delete:
        r=register_to_delete.first()
        r.delete()
    return redirect(request.META.get('HTTP_REFERER'))


        