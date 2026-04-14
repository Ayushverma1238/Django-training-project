from django.contrib import admin
from .models import Contact, Product, Wishlist, Cart, CartItem
# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)