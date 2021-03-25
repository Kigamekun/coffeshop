from django.db import models

from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="media/",blank=True)

    def save(self):
        self.slug = slugify(self.name)
        super(Item,self).save()


    def __str__(self):
        return self.name

  
class Order(models.Model):
    nama = models.PositiveIntegerField()
    total = models.PositiveIntegerField(default=0)
    dibayar = models.PositiveIntegerField(default=0)
    kembali = models.PositiveIntegerField(default=0)
    selesai = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.nama)
    
    
class Cart(models.Model):
    order = models.ForeignKey(Order,related_name='order_item',on_delete=models.CASCADE)
    menu = models.ForeignKey(Item,related_name="menu_item",on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    harga = models.PositiveIntegerField(default=0)
    subtotal = models.PositiveIntegerField(default=0)
    catatan = models.CharField(max_length=200, blank=True, null=True)
    dikirim = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}/{}'.format(str(self.order.nama),self.menu.name)
    

    
    