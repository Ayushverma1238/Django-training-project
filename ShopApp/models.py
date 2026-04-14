from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    phoneNo = models.CharField(max_length=20)
    message = models.CharField(max_length=400)

    def __str__(self):
        return self.email
    

class Product(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank = True)
    imageUrl = models.CharField(max_length=500, null = True, blank=True)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    desc = models.TextField()
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.cart.user} - {self.product.title} ({self.quantity})"