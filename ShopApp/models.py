from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    phoneNo = models.CharField(max_length=20)
    message = models.CharField(max_length=400)

    def __str__(self):
        return self.email
    

class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    desc = models.TextField()
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.title

