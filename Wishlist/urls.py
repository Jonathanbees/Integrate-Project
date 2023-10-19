from django.urls import path
from . import views

app_name = 'Wishlist'

urlpatterns = [
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('ver_wishlist/', views.ver_wishlist, name='ver_wishlist'),
    path('delete_stay/<int:product_id>/', views.delete_stay, name='delete_stay'),
]