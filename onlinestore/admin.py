
from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.html import mark_safe

class Usuarioadmin(admin.ModelAdmin):
    list_display= ("idcomprador","nombre", "usuario", "preferencias")
    search_fields = ("nombre", "usuario")
class Categoriaadmin(admin.ModelAdmin):
    list_display= ("idcategoria","nombre")
    search_fields = ("idcategoria", "nombre")
class DetalleCarritoadmin(admin.ModelAdmin):
    list_display= ("iddetalle","producto_idproducto", "comprador_idcomprador","precioproducto", "subtotal")
    search_fields = ("iddetalle","producto_idproducto", "comprador_idcomprador", "precioproducto", "subtotal")
class Empresaadmin(admin.ModelAdmin):
    list_display= ("idempresa","rut", "nombre", "telefono", "direccion", "mensaje")
    search_fields = ("idempresa","rut", "nombre", "telefono", "direccion", "mensaje")
class Listadeseoadmin(admin.ModelAdmin):
    list_display= ("producto_idproducto","comprador_idcompradores","idlista")
    search_fields = ("producto_idproducto","comprador_idcompradores","idlista")
class Productoadmin(admin.ModelAdmin):
    list_display= ("foto","nombre","codigo", "descripcion", "precio","preciocompra", "cantidad", "etiquetas", "fechavencimiento", "categoria_idcategoria")
    search_fields = ("codigo", "descripcion", "precio", "cantidad", "etiquetas")

admin.site.register(Comprador, Usuarioadmin)
admin.site.register(Categoria, Categoriaadmin)
admin.site.register(Detallecarrito, DetalleCarritoadmin)
admin.site.register(Producto, Productoadmin)