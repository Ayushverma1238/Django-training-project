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
    # path('add_products/', views.addProduct, name="addProduct"),
    path('logout/', views.logoutView, name="logout"),
]