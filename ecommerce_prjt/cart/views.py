from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render,redirect
from home.models import *
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def c_id(request):
    ct_id=request.session.session_key           #if session key is exist,assign it to ct_id

    if not ct_id:                               # means if ct_id = none
        ct_id = request.session.create()        #  there is no session key,then create new one,assidn it ct_id
    return ct_id

@login_required(login_url='login')  #c/n  #login url for when user is not authenticated...it redirect to login

def add_cart(request,product_id):                     #views for adding items to cart
    prod = products.objects.get(id=product_id)
    user = request.user     #c/n
    try:
        ct=cartlist.objects.get(user=user)         #already existing user,fetch userdetails from cartlist & store to ct

    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request),user=user)     #creating new user by calling c_id function for ct_id and assign user to user
        ct.save()

    try:
        c_items = items.objects.get(prod=prod,cart=ct)     #same product existing
        if c_items.quan < c_items.prod.stock:
            c_items.quan += 1    #quan = quan + 1
            prod.stock -= 1
            prod.save()

        c_items.save()                                     #items

    except items.DoesNotExist:
        c_items = items.objects.create(prod=prod,quan=1,cart=ct)
        prod.stock -= 1
        prod.save()
        c_items.save()

    return redirect('cartDetails')


def cart_details(request,tot=0,count=0):        #tot means price,count=item count
    try:
        user = request.user

        if user.is_authenticated:
            ct = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct = cartlist.objects.filter(cart_id=cart_id)
      #----------------------------------------------------

        ct_items = items.objects.filter(cart__in=ct, active=True)
        for i in ct_items:
            tot += (i.prod.price * i.quan)
            count += i.quan

    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty cart');window.location='/';</script>")

    return render(request,'cart.html',{'ci':ct_items,'t':tot,'cn':count})

@login_required(login_url='login')
def min_cart(request,product_id):                 #view for minus_sign in quantity for decreament
    user = request.user
    try:
        if user.is_authenticated:
            ct_list= cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct_list = cartlist.objects.filter(cart_id=cart_id)
        if ct_list.exists:
            for ct in ct_list:
                pro=get_object_or_404(products,id=product_id)
                try:
                    c_items=items.objects.get(prod=pro,cart=ct)
                    if c_items.quan>1:
                        c_items.quan -=1
                        c_items.save()
                    else:
                        c_items.delete()
                except cartlist.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')
@login_required(login_url='login')
def cart_delete(request,product_id):
    user = request.user
    try:
        if user.is_authenticated:
            ct_list = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct_list = cartlist.objects.filter(cart_id=cart_id)

        if ct_list.exists():
            for ct in ct_list:
                prod = get_object_or_404(products,id=product_id)
                try:
                    c_items = items.objects.get(prod=prod, cart=ct)
                    c_items.delete()
                except items.DoesNotExist:
                    pass

    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')


def check_out(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        country = request.POST['country']
        address = request.POST['address']
        towncity = request.POST['city']
        postcodezip = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        cart = cartlist.objects.filter(user=request.user).first()

        check = checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            towncity=towncity,
            postcodezip=postcodezip,
            phone=phone,
            email=email,
        )
        print(check)
        check.save()
        return redirect('payment')
    return render(request,'checkout.html')

def payment(request):
    return render(request,'bank.html')

def success(request):
    return render(request,'successful.html')

def shop(request):
    return render(request,'shop.html')