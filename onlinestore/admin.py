from django.contrib import admin
from .models import *

class Usuariosadmin(admin.ModelAdmin):
    list_display= ("id","nombre", "email", "direccion", "telefono")
    search_fields = ("nombre", "telefono")
class Categoriaadmin(admin.ModelAdmin):
    list_display= ("id","nombre", "descripcion")
    search_fields = ("nombre", "descripcion")

admin.site.register(Cliente, Usuariosadmin)
admin.site.register(Categoria, Categoriaadmin)
