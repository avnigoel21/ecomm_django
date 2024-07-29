from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Category)
admin.site.register(Coupon)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display= ['product_name', 'price']
    inlines = [ProductImageAdmin]

@admin.register(ColorVariant)
class ColorVariant(admin.ModelAdmin):
    list_display= ['color_name', 'price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariant(admin.ModelAdmin):
    list_display= ['size_name', 'price']
    model = SizeVariant

admin.site.register(Product, ProductAdmin)


admin.site.register(ProductImage)

