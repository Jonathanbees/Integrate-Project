
from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.html import mark_safe

class Buyeradmin(admin.ModelAdmin):
    list_display= ("idbuyer","name", "preferences", "email")
    search_fields = ("name", "username")
class Categoryadmin(admin.ModelAdmin):
    list_display= ("idcategory","name")
    search_fields = ("idcategory", "name")
class Cartadmin(admin.ModelAdmin):
    readonly_fields= ("iddetails","product_idproduct", "buyer_idbuyer","product_units", "subtotal")
    search_fields = ("iddetails","product_idproduct", "buyer_idbuyer","product_units", "subtotal")
class Companyadmin(admin.ModelAdmin):
    list_display= ("idcompany","rut", "name", "phone_number", "address", "message")
    search_fields = ("idcompany","rut", "name", "phone_number", "address")
class Wishlistadmin(admin.ModelAdmin):
    readonly_fields= ("idwishlist","product_idproduct","buyer_idbuyer")
    search_fields = ("idwishlist","product_idproduct","buyer_idbuyer")
"""
def dividebrand(obj):
    return (obj.split(",")).lower()
"""
class Productadmin(admin.ModelAdmin):
    list_display= ("idproduct","name","code","description","purchase_price","sale_price", "available_quantity", "tags", "expiration_date","brand","category_idcategory", "image")
    search_fields = ("name","code","description","available_quantity", "tags", "expiration_date","brand")
class Purchasesadmin(admin.ModelAdmin):
    list_display= ("idpurchases", "date", "total")
    search_fiels= ("idpurchase", "date")
class Orderadmin(admin.ModelAdmin):
    readonly_fields= ("idorder", "status","products_amount","transaction_date", "subtotal")
    search_fiels= ("idorder", "status","transaccion_date")
class ProductOrderadmin(admin.ModelAdmin):
    readonly_fields = ("idproducto_order", "product_idproduct","order_idorder","quantity")
    search_fields = ("idproducto_order", "product_idproduct","order_idorder","quantity")


admin.site.register(Buyer, Buyeradmin)
admin.site.register(Category, Categoryadmin)
admin.site.register(Cart, Cartadmin)
admin.site.register(Product, Productadmin)
admin.site.register(Wishlist, Wishlistadmin)
admin.site.register(Order, Orderadmin)
admin.site.register(ProductOrder,ProductOrderadmin)

