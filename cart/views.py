from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from onlinestore.models import Buyer, Category, Product, Cart

@login_required
def add_to_cart(request, product_id):
    user_profile = get_object_or_404(Buyer,idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    
    if  user_profile and product:
        Cart_entrance, created = Cart.objects.get_or_create(buyer_idbuyer=user_profile, product_idproduct=product)
        if not created:
            Cart_entrance.product_units += 1
            Cart_entrance.subtotal = product.sale_price*Cart_entrance.product_units        
        else:
            Cart_entrance.product_units = 1
            Cart_entrance.subtotal = product.sale_price
        Cart_entrance.save()
        cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
        products = []
        total = 0
        for i in cartproduct:
            p = get_object_or_404(Product, pk=i.product_idproduct)
            p.subtotal = i.subtotal
            total += i.subtotal
            p.product_units = i.product_units
            products.append(p)
        return render(request,'detail.html', {'cart': products, 'total': total})

    
    