from django.shortcuts import render, redirect, get_object_or_404
from onlinestore.models import Product, Cart, CartItem
"""
def cart_add(request, product_id):
    products = Product.objects.order_by('name')
    #Buscador
    searchTerm = request.GET.get("searchProduct") #se recoge el input del buscador
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)
    categories = Category.objects.order_by('name')


    form = CartAddProductForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        request.session['cart'] = cart
        return redirect('cart:cart_detail')
    
    return render(request, 'cart/add.html', {'products': products, 'categories':categories,'allcategories':categories, 'form': form})

def cart_detail(request):
    cart = request.session.get('cart', {})
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total += quantity * product.price
    return render(request, 'cart/detail.html', {'cart': cart, 'total': total})
"""
def cart_detail(request):
    cart = Cart.objects.get(id=request.session['cart_id'])
    context = {'cart': cart}
    return render(request, 'cart/detail.html', context)

def add_to_cart(cart, request, product_id):
    cart = Cart.objects.get(id=request.session['cart_id'])
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.line_item_total += product.price
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product)
    cart.total += product.price
    cart.save()
    return redirect('cart:cart_detail')