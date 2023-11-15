from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('create_order/',views.create_order,name='create_order'),
    path('cancel_order/<int:idorder>',views.cancel_order,name='cancel_order'),
    path('order/<int:idorder>', views.see_order, name='see_order'),
    path('orders/',views.see_orders,name='see_orders'),
    path('pay_order/<int:idorder>',views.pay_order,name='pay_order'),

]