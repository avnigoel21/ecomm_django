from django.contrib import admin
from django.urls import path
from accounts.views import *

urlpatterns = [
    path('login/', login_page)
]