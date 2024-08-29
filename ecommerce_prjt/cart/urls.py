from django.urls import path
from .import views

urlpatterns = [

    path('cartDetails/',views.cart_details,name='cartDetails'),
    path('add/<int:product_id>/',views.add_cart,name='addcart'),
    path('min/<int:product_id>/',views.min_cart,name='mincart'),
    path('cartDelete/<int:product_id>/',views.cart_delete,name='cartDelete'),
    path('checkout',views.check_out,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('successful/',views.success,name='successful'),
    path('shopping/',views.shop,name='shopping'),
]