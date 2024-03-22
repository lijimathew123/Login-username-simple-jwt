from django.db import models
from account_app.models import *
from company.models import *

# Create your models here.
import uuid

class Customer(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
     created_by = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE)
     created_at = models.PositiveIntegerField(null=True, blank=True)
     last_modified_at = models.PositiveIntegerField()
     company = models.ForeignKey(Company, on_delete=models.CASCADE)
     
     

     class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customer"



class DefaultCustomerCategory(models.Model):
    name = models.CharField(max_length=25)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Default customer category"
        verbose_name_plural = "Default customer category"

class DefaultCustomerFields(models.Model):
    catogory  = models.ForeignKey(DefaultCustomerCategory, on_delete = models.CASCADE)
    field_type = models.ForeignKey(FieldType, on_delete = models.CASCADE)
   
    display_name =models.CharField(max_length=55)
    mem_variable = models.CharField(max_length=50)
    options = ArrayField(models.CharField(max_length=900), blank=True)
    regex_field = models.CharField(max_length=500, default="",blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    required = models.BooleanField(default=False)
    is_quick = models.BooleanField(default=False)
    is_static = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Default Customer field"
        verbose_name_plural = "Default Customer field"

