import random
import string

import stripe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from pprint import pprint
from django.views.generic import ListView, DetailView, View
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import *
from .forms import *

from django.contrib.auth.decorators import user_passes_test


def index(request):
    return render(request,'core.html')
def handler404(request, exception):

    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    context = {}
    response = render(request, "500.html", context=context)
    response.status_code = 500
    return response


@login_required


@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='/')
def create(request):
    forms = ItemForms(request.POST,request.FILES)
    if request.method == "POST":
        if forms.is_valid():
            forms.save()
            messages.success(request, 'Item Created.')
            return redirect('core:pricing')
        else :
            messages.success(request, 'Invalid add Item.')
            return redirect('core:create')
    context = {
		'forms':forms
	}
    return render(request,'create.html',context)
        

def about(request):
    return render(request,'about.html')
class HomeView(ListView):
    model = Item
    paginate_by = 6
    template_name = "home.html"


@login_required

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='/')
def delete(request,delete_id):
    Item.objects.filter(id = delete_id).delete()
    messages.success(request,'Data Deleted')
    return redirect('core:pricing')


@login_required

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='/')
def update(request,update_id):
	obj = Item.objects.get(id=update_id)
	data = {
	'name':obj.name,	
	'price':obj.price,
	'slug':obj.slug,
	'description':obj.description,
	'image':obj.image
	}

	forms = ItemForms(request.POST or None,request.FILES or None , initial= data,instance=obj)
	if request.method == 'POST':
		if forms.is_valid():
			messages.success(request, 'Data Updated.')
			forms.save()
			return redirect('core:pricing')
	context = {
	'page_title':'Update',
	'forms':forms,
	'obj':obj
	}
	return render(request,'create.html',context)


def detail(request,detail_id):
    data = Item.objects.get(id = detail_id)
    return render(request,'detail.html',{'data':data})
    
    
@login_required
def add_to_cart(request,item_id):
    
    item_order = Item.objects.get(id = item_id)
    # item_order = get_object_or_404(Item, id=item_id)
    pelanggan ,created = Order.objects.get_or_create(
        nama = request.user.id
    )
    
    
    
    item, created = Cart.objects.get_or_create(
        menu=item_order,
        order=pelanggan
    )
    
    item.qty = item.qty + 1
    item.harga = item_order.price
    item.subtotal = item.harga * item.qty
    item.save()

    orders = Cart.objects.filter(order=pelanggan).aggregate(total=Sum('subtotal'))
    pelanggan.total = orders['total']
    pelanggan.save()
    messages.success(request, 'Success Add item.')
    return redirect('core:pricing')


@login_required
def cart(request):
    try:

        menu_list = Item.objects.all()
        order = get_object_or_404(Order, nama=request.user.id)

        page = request.GET.get('page', 1)
    
        paginator = Paginator(menu_list, 10)
    
        try:
            menus = paginator.page(page)
        except PageNotAnInteger:
            menus = paginator.page(1)
        except EmptyPage:
            menus = paginator.page(paginator.num_pages)
    
        return render(request, 
                  'cart.html', 
                  {'menus': menus,
                   'order': order})
    except:
        return render(request,'cart.html')


@login_required
def delete_to_cart(request,item_name):
    item_order = Item.objects.get(id = item_name)
    pelanggan ,created = Order.objects.get_or_create(
        nama = request.user.id
    )
    item, created = Cart.objects.get_or_create(
        menu=item_order,
        order=pelanggan
    )
    
    item.qty -= 1 

    if item.qty <= 0 :
        item.delete()
        orders = Cart.objects.filter(order=request.user.id).aggregate(total=Sum('subtotal'))
        pelanggan.total -= item_order.price
        pelanggan.save()
        if pelanggan.total == 0 :
            pelanggan.delete()
        
    
    else :

        print("heii",request.user.id)
        item.harga = item_order.price
        item.subtotal = item.harga * item.qty
        item.save()
      
        orders = Cart.objects.filter(order=pelanggan).aggregate(total=Sum('subtotal'))
        print("heiii",orders['total'])
        pelanggan.total = orders['total']
        pelanggan.save()
    
  
    messages.success(request, 'Success delete item.')
    return redirect('core:cart')

@login_required

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='/')
def order_aktif(request):
    order_list = Order.objects.filter(selesai=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(order_list, 10)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    names = []
    for solve in order_list :
        name = User.objects.get(id=solve.nama)
        names.append(name.username)
    mylist = zip(orders, names)
    return render(request,
                  'order_aktif.html',
                  {'orders': orders,'names':names,'mylist':mylist})

