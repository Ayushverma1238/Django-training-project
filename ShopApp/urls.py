from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.loginView, name="login"),
    path('signUp/', views.signupView, name="signUp"),
    path('product/', views.product, name="product"),
    path('logout/', views.logoutView, name="logout"),

    # ✅ Wishlist
    path('wishlist/', views.wishlist, name="wishlist"),
    path('cart/', views.cart_view, name='cart'),

    # ✅ ADD THESE 👇
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove-wishlist/<int:id>/', views.remove_from_wishlist, name="remove_from_wishlist"),

    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('update-cart-qty/', views.update_cart_qty, name='update_cart_qty'),    # (optional)
    path('add-to-cart/<int:id>/', views.add_to_cart, name="add_to_cart"),

    # Path for women, man,kids
    path('womens-collection/', views.women, name="women"),
    path('mens-collection/', views.men, name="men"),
    path('kids-collection/', views.kids, name="kids"),

]