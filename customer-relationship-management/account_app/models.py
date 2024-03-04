from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


AbstractUser._meta.get_field('username').null=True

# Create your models here.
class CustomerType(models.Model):
   type = models.CharField(max_length=255)

   def __str__(self):
       return self.type

   class Meta:
        verbose_name = "Customer Type"
        verbose_name_plural = "Customer Type"


class PlatformCustomer(AbstractUser):

    phone = models.CharField(null=False, blank=False, max_length=15)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=255)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    

    last_login = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    def verify_phone(self):
        self.is_phone_verified = True
        self.save()

    def update_last_login(self, ip_address=None):
        self.last_login = timezone.now()
        self.last_login_ip = ip_address
        self.save()


    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Platform Customer"
        verbose_name_plural = "Platform Customer"


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


   

class PlatformCustomerDetails(models.Model):
    customer = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='profiles/')
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    linkedin = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    x = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    theme = models.IntegerField()
  
     
    def __str__(self):
        return self.customer.email if self.customer else "No Customer Assigned"
    
    class Meta:
        verbose_name = "Platform Customer Details"
        verbose_name_plural = "Platform Customer Details"


class Organization(models.Model):
    owner = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE,default="")
    organization_name = models.CharField(max_length=30)
    business_type = models.CharField(max_length=25)
    industry_type = models.CharField(max_length=25)
    logo = models.ImageField(upload_to='logos/')
    banner = models.ImageField(upload_to='banners/')
    address = models.TextField()
    location= models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    email=models.CharField(max_length=40)
    phone=models.CharField(max_length=12,null=False, blank=False, unique=True)
    website=models.CharField(max_length=40)
    linkedin = models.CharField(max_length=40)
    facebook = models.CharField(max_length=40)
    instagram=models.CharField(max_length=40)
    x_address=models.CharField(max_length=40)
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.organization_name
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organization"


class OrganizationBranch(models.Model):
    
    organization_name=models.ForeignKey(Organization, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    address=models.TextField()
    email = models.EmailField(max_length=25)
    phone=models.CharField(max_length=12,null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branch"

   

