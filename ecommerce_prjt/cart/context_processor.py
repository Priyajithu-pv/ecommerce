from . views import *
from home.views import *


def cate(request):       #view for display category droplist in all templates
    obj2 = categ.objects.all()      # use same variable as index in home/views
    return{'j':obj2}                # same context as in view.index in home

def cart_total(request):
    tot = 0
    count = 0

    user = request.user
    if user.is_authenticated:
        ct = cartlist.objects.filter(user=user)
    else:
        cart_id = request.session.get('cart_id')
        ct = cartlist.objects.filter(cart_id=cart_id)

    ct_items = items.objects.filter(cart__in=ct, active=True)

    for i in ct_items:
        tot += (i.prod.price * i.quan)
        count += i.quan

    return {'t': tot, 'cn': count}
