from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from onlinestore.models import Buyer, Product, Cart

@login_required
def add_to_cart(request, product_id):
    user_profile = get_object_or_404(Buyer, idbuyer=request.user.id)
    product = get_object_or_404(Product, pk=product_id)
    if user_profile and product:
        cart_entry = Cart.objects.filter(buyer_idbuyer=user_profile, product_idproduct=product_id).first()
        if cart_entry:
            if cart_entry.product_units < product.available_quantity:
                cart_entry.product_units += 1
                cart_entry.subtotal = product.sale_price * cart_entry.product_units
                cart_entry.save()
        else:
            Cart.objects.create(
                buyer_idbuyer=user_profile,
                product_idproduct=product_id,
                product_units=1,
                subtotal=product.sale_price
                )
        cartproduct= Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
        products = []
        total = 0
        
        for i in cartproduct:
            p = get_object_or_404(Product, pk=i.product_idproduct)
            p.subtotal = i.subtotal
            total += i.subtotal
            p.product_units = i.product_units
            products.append(p)
        return render(request,'detail.html', {'cart': products, 'total':total})
    
    