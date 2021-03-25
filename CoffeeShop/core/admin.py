from django.contrib import admin

# Register your models here.
from .models import *

class itemadmin(admin.ModelAdmin):
    list_display = ['name','price','slug']
    search_fields = ['name','price','slug']
    list_per_page = 15
admin.site.register(Item,itemadmin)

class orderadmin(admin.ModelAdmin):
    list_display = ['nama','total','dibayar','kembali','selesai']
    search_fields = ['nama']
    list_per_page = 15
admin.site.register(Order,orderadmin)


class cartadmin(admin.ModelAdmin):
    list_display = ['order','menu','qty','harga','subtotal']
    list_per_page = 15
admin.site.register(Cart,cartadmin)
