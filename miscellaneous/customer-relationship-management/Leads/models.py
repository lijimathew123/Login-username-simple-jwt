from django.db import models
from account_app.models import Organization,PlatformCustomer

# Create your models here.
class Role(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Role"



    
class CustomerRole(models.Model):
    role=models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE)


    def __str__(self):
        return self.role.name if self.role else "No Customer Role"
    

    class Meta:
        verbose_name = "Customer Role"
        verbose_name_plural = "Customer Role"

    
        
    
        