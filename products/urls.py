from django.contrib import admin
from django.urls import path
from products.views import *

urlpatterns = [
    path('', get_product),
   
]