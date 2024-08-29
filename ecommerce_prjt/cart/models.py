from django.db import models
from home.models import *       # we call the model in the shop that is product and category
from django.contrib.auth.models import User     #importing the User table

# Create your models here.


class cartlist(models.Model):               #Table for userdetails and cartdetails, who is using the cart
    cart_id=models.CharField(max_length=250,unique=True)
    date_added=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, default=None)   #c/u

    def __str__(self):
        return self.cart_id

#Details of product items which are in cart
class items(models.Model):
    prod=models.ForeignKey(products,on_delete=models.CASCADE)  #Here class/table product from shop ia act as a foreign key so we
    cart=models.ForeignKey(cartlist,on_delete=models.CASCADE)
    quan=models.IntegerField()
    active=models.BooleanField(default=True)
    def __str__(self):
        return str(self.prod)
    def total(self):
        return self.prod.price*self.quan

class checkout(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    cart = models.ForeignKey(cartlist, on_delete=models.CASCADE,null=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    address=models.TextField(max_length=200)
    towncity=models.CharField(max_length=100)
    postcodezip=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)
    email=models.EmailField()