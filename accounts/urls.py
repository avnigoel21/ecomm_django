from django.contrib import admin
from django.urls import path
from accounts.views import *
from products.views import *

urlpatterns = [
    path('login/', login_page),
    path('register/', register_page),
    path('activate/<email_token>/',activate_email),
   # path('cart/', cart , name = "cart"),
    path('add-to-cart/<uid>' , add_to_cart, name = "add_to_cart")
]