from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart_stay/<int:product_id>/', views.add_to_cart_stay, name='add_to_cart_stay'),
    path('reduce_one/<int:product_id>/', views.reduce_one, name='reduce_one'),
    path('delete/<int:product_id>/', views.delete, name='delete'),
    path('delete_stay/<int:product_id>/', views.delete_stay, name='delete_stay'),
    path('cart/',views.cart,name='cart')
]