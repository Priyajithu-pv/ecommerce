from django.db import models
from django.urls import reverse

# Create your models here.
class categ(models.Model):
    name=models.CharField(max_length=200,unique=True)
    slug= models.SlugField(max_length=200,unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('product_cate',args=[self.slug])

class products(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    img = models.ImageField(upload_to='product')
    desc = models.TextField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField()
    price = models.IntegerField()
    category = models.ForeignKey(categ,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('details',args=[self.category.slug,self.slug])