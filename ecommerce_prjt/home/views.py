from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from . models import *

# Create your views here.

def index(request,cslug = None ):        #cslug=kid
    if cslug != None:
        cpro = get_object_or_404(categ,slug=cslug)  #for getting the category selected
        obj = products.objects.all().filter(category=cpro)  #for getting the products of selected product
    else:
        obj = products.objects.all()

    obj2 = categ.objects.all()

    var = Paginator(obj,8)
    pgnum = int(request.GET.get('page',1))

    try:
        doc = var.page(pgnum)
    except (InvalidPage,EmptyPage):
        doc = var.page(var.num_pages)

    return render(request,'index.html',{'i':obj, 'j':obj2, 'var':doc})

#search button in nav bar of base.html
def search(request):
    if 'q' in request.GET:
        query = request.GET.get('q');
        obj1 = products.objects.all().filter(Q(name__icontains=query)|Q(desc__icontains=query))
        print(obj1,"****")

        if not obj1:
            print("No matching results")

    return render(request,'search.html',{'p':obj1})


# to display product details in product-single.html
def details(request,cslug,pslug):
    prodt = products.objects.get(category__slug = cslug,slug = pslug)
    return render(request,'product-single.html',{'c':prodt})

#for about page
def about(request):

    return render(request,'about.html')

# to display contact details
def contact(request):

    return render(request,'contact.html')

# to display blog
def blog(request):

    return render(request,'blog.html')