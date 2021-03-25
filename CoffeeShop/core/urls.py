from django.urls import path
from .views import *
from django.conf.urls import handler404,handler500
app_name = 'core'

urlpatterns = [
    path('',index,name='home'),
    path('pricing/', HomeView.as_view(), name='pricing'),
    path('update/<update_id>',update , name="update"),
    path('delete/<delete_id>',delete , name="delete"),
    path('about/',about,name="about"),
    path('detail/<detail_id>',detail,name="detail"),
    path('create/',create,name="create"),

    path("add_to_cart/<item_id>", add_to_cart, name="add_to_cart"),
    path("delete_to_cart/<item_name>", delete_to_cart, name="delete_to_cart"),
    path("cart/", cart, name="cart"),
    path('order-aktif/', order_aktif, name='order-aktif'),
    
]


handler404 = 'core.views.handler404'

handler500 = 'core.views.handler500'

