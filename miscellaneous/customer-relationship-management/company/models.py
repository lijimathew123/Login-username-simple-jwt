from django.db import models
from account_app.models import *

import uuid
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)
    created_by = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE)
    created_at = models.PositiveIntegerField()
    last_modified_at = models.PositiveIntegerField()


    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"





class DefaultCompanyCategory(models.Model):
    name = models.CharField(max_length=25)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Default company category"
        verbose_name_plural = "Default company category"



class DefaultCompanyFields(models.Model):

    catogory  = models.ForeignKey(DefaultCompanyCategory, on_delete = models.CASCADE)
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
        verbose_name = "Default Company field"
        verbose_name_plural = "Default Company field"



