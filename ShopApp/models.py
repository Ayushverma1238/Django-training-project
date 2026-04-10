from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    phoneNo = models.CharField(max_length=20)
    message = models.CharField(max_length=400)

    def __str__(self):
        return self.name
    
