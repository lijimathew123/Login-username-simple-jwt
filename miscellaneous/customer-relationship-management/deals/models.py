from django.db import models

from account_app.models import * 
from Leads.models import *
import uuid

class Deals(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
     owner = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE)
     name = models.CharField(max_length=100)
     created_at = models.PositiveIntegerField()
     last_stage_modified = models.PositiveIntegerField()
     leads = models.ForeignKey(Leads, on_delete=models.CASCADE)
     stage = models.PositiveIntegerField()
     probability = models.PositiveIntegerField()

     class Meta:
        verbose_name = "Deals"
        verbose_name_plural = "Deals"



class DefaultDealStatus(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     stage = models.CharField(max_length=20)
     probability = models.PositiveIntegerField()
     order  = models.PositiveIntegerField()




class DefaultDealCategory(models.Model):
    name = models.CharField(max_length=25)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Default deal category"
        verbose_name_plural = "Default deal category"

class DefaultDealFields(models.Model):
    catogory  = models.ForeignKey(DefaultDealCategory, on_delete = models.CASCADE)
    field_type = models.ForeignKey(FieldType, on_delete = models.CASCADE)
   
    display_name =models.CharField(max_length=55)
    mem_variable = models.CharField(max_length=50)
    options = ArrayField(models.CharField(max_length=900), blank=True)
    regex_field = models.CharField(max_length=500, default="", blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    is_quick = models.BooleanField(default=False)
    is_static = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Default deal field"
        verbose_name_plural = "Default Deal field"

