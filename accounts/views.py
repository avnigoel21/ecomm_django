from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from products.models import Coupon, Product, SizeVariant
from .models import Cart, CartItems, Profile
# Create your views here.

def login_page(request):
    if request.method == "POST":
       
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if not user_obj.exists():
            messages.warning(request,"Accound not found.")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request,"Your account is not verified.")
            return HttpResponseRedirect(request.path_info)
        

        user_obj = authenticate(username = email, password = password)
        if(user_obj):
            login(request, user_obj)
            return redirect('/')
       

        messages.success(request, "Invalid Credentials.")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')




def register_page(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request,"Email is already taken.")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "An email has been sent to your mail.")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    
    except Exception as e:
        return HttpResponse("Invalid Email Token")
    


def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid = uid)
    user = request.user

    cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_item = CartItems.objects.create(cart = cart, product = product)

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size_variant
        cart_item.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER') )
    

def remove_cart(request, cart_item_uid):
    pass


def cart(request):
    cart_obj =  Cart.objects.get(is_paid = False, user = request.user)

    if request.method == "POST":
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)

        if not coupon_obj.exists():
            messages.warning(request, "Invalid Coupon.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER') )
        
        if cart_obj.coupon:
            messages.warning(request, "Coupon already exists.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER') )
        
        if cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request, "Amount should be greater than", coupon_obj.minimum_amount)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER') )


        if coupon_obj.is_expired:
            messages.warning(request, "Coupon Expired.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER') )
        
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, "Coupon Applied.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') )
        
    context = {'cart' : cart_obj}
    return render(request, "accounts/cart.html", context)