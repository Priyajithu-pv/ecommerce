from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search',views.search,name='search'),
    path('<slug:cslug>/',views.index,name='product_cate'),
    path('<slug:cslug>/<slug:pslug>', views.details, name='details'),
    path('home/about/',views.about,name='about'),
    path('home/contact_details/',views.contact,name='contact'),
    path('home/blog/',views.blog,name='blog'),

]