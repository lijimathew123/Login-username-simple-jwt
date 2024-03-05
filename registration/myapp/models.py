from django.db import models
from django.contrib.auth.hashers import make_password 

class Employee(models.Model):
    username=models.CharField(max_length=30,default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 


    def save(self, *args, **kwargs):
        # Use make_password to hash the password
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    
