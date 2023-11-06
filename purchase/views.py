from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from onlinestore.models import Buyer, Product, Cart, Category,Order,ProductOrder
import onlinestore.views as onlinestore_views
import cart.views as cart_views
from django.contrib import messages
from datetime import datetime,timedelta
def exceeds_stock(request):
    user_profile=get_object_or_404(Buyer,idbuyer=request.user.id)
    cartproducts=Cart.objects.all().filter(buyer_idbuyer=user_profile.idbuyer)
    for c in cartproducts:
        product = get_object_or_404(Product, pk=c.product_idproduct)
        if c.product_units>product.available_quantity:
            c.product_units+=1
            c.save()
            messages.error(request, 'La cantidad en carrito del producto '+product.name+' excede las unidades disponibles')
            return product.name
    return False

def release_stock():
    all_orders=Order.objects.all().filter(status="pendiente")
    for order in all_orders:
        order.deadline=order.order_date+timedelta(minutes=5)
        if order.deadline<datetime.now():
            registers=ProductOrder.objects.all().filter(order_idorder=order.idorder)
            for register in registers:
                product=get_object_or_404(Product,idproduct=register.product_idproduct)
                product.available_quantity+=register.quantity
                product.save()
                register.delete()
            order.delete()
def purchased_product(request,idproduct):
    buyer=Buyer.objects.get(idbuyer=request.user.id)
    orders=Order.objects.all().filter(buyer_idbuyer=buyer.idbuyer,status="confirmado")
    for order in orders:
        registers=ProductOrder.objects.all().filter(order_idorder=order.idorder,product_idproduct=idproduct)
        if registers:
            return True
    return False
def order_units(request):
    if request.user.is_authenticated:
        buyer=Buyer.objects.get(idbuyer=request.user.id)
        orders=Order.objects.all().filter(buyer_idbuyer=buyer.idbuyer)
        release_stock()
    else:
        return None
    return len(orders)

@login_required
def create_order(request):
    product_exceed=exceeds_stock(request)
    if product_exceed:
        messages.error(request, 'La cantidad en carrito del producto '+product_exceed+' excede las unidades disponibles')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        buyer=Buyer.objects.get(idbuyer=request.user.id)
        cartproducts=Cart.objects.all().filter(buyer_idbuyer=buyer.idbuyer)
        if(len(cartproducts)):
            ready_cart=cart_views.get_cart_ready(cartproducts,request)
            products = ready_cart[0]
            subtotal = ready_cart[1]
            total=ready_cart[2]
            discount=ready_cart[3]
            total_units=ready_cart[4]
            print(datetime.now)
            subtotal=sum([c.subtotal for c in cartproducts])
            order=Order.objects.create(
                buyer_idbuyer=buyer,
                status="pendiente",
                subtotal=subtotal,
                total=total,
                order_date=datetime.now(),
            )
            order.save()
            for register in products:
                product = get_object_or_404(Product, pk=register.idproduct)
                if register.next_to_expire:
                    ProductOrder.objects.create(product_idproduct=product,
                    order_idorder=order,
                    quantity=register.product_units,
                    nondiscounted_unit_price=product.sale_price,
                    discounted_unit_price=register.next_to_expire[1],
                    discount=register.next_to_expire[2]
                    )
                else:
                    ProductOrder.objects.create(product_idproduct=product,
                    order_idorder=order,
                    quantity=register.product_units,
                    nondiscounted_unit_price=product.sale_price,
                    discounted_unit_price=product.sale_price,
                    discount=0
                    )
                product.available_quantity-=register.product_units
                product.save()
            for c in cartproducts:
                c.delete()
            return see_order(request,order.idorder)
        else:
            messages.error(request, 'No se puede generar una orden sin productos en el carro de compras')
            return redirect(request.META.get('HTTP_REFERER'))


@login_required
def see_order(request,idorder):
    order=Order.objects.get(pk=idorder)
    orders=Order.objects.all().filter(pk=idorder,buyer_idbuyer=request.user.id)
    if order in orders:
        order.discount=order.subtotal-order.total
        order.deadline=order.order_date+timedelta(minutes=5)
        registers=ProductOrder.objects.all().filter(order_idorder=order.idorder)
        for register in registers:
            product=get_object_or_404(Product,idproduct=register.product_idproduct)
            register.product=product
            register.subtotal=register.quantity*register.nondiscounted_unit_price
            register.total_discount=register.discount*register.quantity
            register.total=register.subtotal-register.total_discount
        current_time=datetime.now()
        demora = int((order.deadline - current_time).total_seconds())
        if order.status=="pendiente":
            order.paid=False
        else:
            order.paid=True
        return render(request,'order.html',{'order':order,'registers':registers,'demora':demora,'order_units':order_units(request),'total_units':cart_views.units_cart(request)})
    else:
        return onlinestore_views.index(request)
@login_required
def cancel_order(request,idorder):
    order=Order.objects.get(pk=idorder)
    orders=Order.objects.all().filter(pk=idorder,buyer_idbuyer=request.user.id)
    if order in orders:
        registers=ProductOrder.objects.all().filter(order_idorder=order.idorder)
        for register in registers:
            product=get_object_or_404(Product,idproduct=register.product_idproduct)
            product.available_quantity+=register.quantity
            product.save()
            register.delete()
        order.discount=order.subtotal-order.total
        order.deadline=order.order_date+timedelta(minutes=5)
        if order.deadline<datetime.now():
            messages.error(request, 'Se ha cancelado tu order con fecha de  por exceder el tiempo de espera del pago')
        else:
            messages.success(request, 'Se ha cancelado la orden de manera exitosa')
        order.delete()
        return redirect('purchase:see_orders')
    else:
        return onlinestore_views.index(request)
@login_required
def see_orders(request):
    buyer=Buyer.objects.get(idbuyer=request.user.id)
    orders=Order.objects.all().filter(buyer_idbuyer=buyer.idbuyer).order_by('-order_date')
    for order in orders:
        if order.status=="pendiente":
            order.paid=False
            order.deadline=order.order_date+timedelta(minutes=5)
            order.demora=int((order.deadline-datetime.now()).total_seconds())
        else:
            order.paid=True
    return render(request,'purchases.html',{'orders':orders,'order_units':order_units(request),'total_units':cart_views.units_cart(request)})

@login_required
def pay_order(request,idorder):
    order=Order.objects.get(pk=idorder)
    orders=Order.objects.all().filter(pk=idorder,buyer_idbuyer=request.user.id)
    if order in orders:
        order.transaction_date=datetime.now()
        order.status='confirmado'
        order.method="Transaccion bancaria"
        order.save()
        registers=ProductOrder.objects.all().filter(order_idorder=order.idorder)
        for register in registers:
            product=get_object_or_404(Product,idproduct=register.product_idproduct)
            product.quantity_sold+=register.quantity
            product.save()
        buyer=Buyer.objects.get(idbuyer=request.user.id)
        orders=Order.objects.all().filter(buyer_idbuyer=buyer.idbuyer)
        return see_order(request,order.idorder)
    else:
        return onlinestore_views.index(request)






        

