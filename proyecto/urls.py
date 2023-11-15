"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from onlinestore import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('admin/', views.admin, name='admin'),
    path('category/<int:category_id>/',views.category , name='category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('', include('accounts.urls')),
    path('offers/', views.expiration_offers,name='offers'),
    path('cart/', include('cart.urls')),
    path('wishlist/', include(('Wishlist.urls', 'wishlist'), namespace='wishlist')),
    path('purchase/', include(('purchase.urls'))),
<<<<<<< HEAD
=======
    path('graphics/', views.graphics, name='graphics'),

>>>>>>> 6495cf22387e2e518e4fba3585910ccf0e32fe75
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)