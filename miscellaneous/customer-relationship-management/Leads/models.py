from django.db import models
from account_app.models import Organization,PlatformCustomer

from company.models import *
from customer.models import * 
import uuid





class Leads(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE)
    
    created_at = models.PositiveIntegerField()
    last_modified_at = models.PositiveIntegerField()
   
    # converted_to_customer = models.BooleanField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank = True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank= True, null=True)
    

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Lead"



class DefaultLeadCategory(models.Model):
    name = models.CharField(max_length=25)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Default lead category"
        verbose_name_plural = "Default lead category"




class DefaultLeadFields(models.Model):
    catogory  = models.ForeignKey(DefaultLeadCategory, on_delete = models.CASCADE)
    field_type = models.ForeignKey(FieldType, on_delete = models.CASCADE)
    display_name =models.CharField(max_length=55)
    mem_variable = models.CharField(max_length=50)
    options = ArrayField(models.CharField(max_length=900),blank=True)
    regex_field = models.CharField(max_length=500, default="", blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    is_quick = models.BooleanField(default=False)
    is_static = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Default lead field"
        verbose_name_plural = "Default lead field"


