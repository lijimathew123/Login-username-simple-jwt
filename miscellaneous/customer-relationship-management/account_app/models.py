import uuid
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


class SocialChannel(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     icon = models.ImageField(upload_to='icons/')
     name = models.CharField(max_length=255)
     order = models.IntegerField()

     def __str__(self):
         return self.name


     class Meta:
        verbose_name = "Social Channel"
        verbose_name_plural = "Social Channel"


class PlatformCustomer(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(null=False, blank=False, max_length=15)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=255, default="website")
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
   
    
    def verify_phone(self):
        self.is_phone_verified = True
        self.save()

    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Platform Customer"
        verbose_name_plural = "Platform Customer"





class PlatformCustomerSocialChannels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE, related_name='social_channels')
    social_channel = models.ForeignKey(SocialChannel, on_delete=models.CASCADE, related_name='customer_profiles')
    profile_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Platform customer social profile"
        verbose_name_plural = "Platform customer social profile"

    def __str__(self):
        return f"{self.customer} - {self.social_channel}"




class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)




class UserLastLogin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(PlatformCustomer, on_delete=models.CASCADE)
    last_login = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Last login of {self.user.email}"
    

class Theme(models.Model):
    style = models.JSONField()   
   

class PlatformCustomerDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(PlatformCustomer, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=25)
    phone_2 = models.CharField(max_length=15)
    dob = models.DateField()
    image = models.ImageField(upload_to='profiles/')
    address = models.JSONField()
    state = models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    currency=models.CharField(max_length=20)
    date_format = models.CharField(max_length=35)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)
  
     
    def __str__(self):
        return self.customer.email if self.customer else "No Customer Assigned"
    
    class Meta:
        verbose_name = "Platform Customer Details"
        verbose_name_plural = "Platform Customer Details"


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(PlatformCustomer, related_name='platform_customer_owner', on_delete=models.CASCADE,default="")
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
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.organization_name
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organization"


class CustomerOrganization(models.Model):
    customer = models.ForeignKey(PlatformCustomer, on_delete = models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)



class OrganizationBranch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_name=models.ForeignKey(Organization, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    address=models.TextField()
    email = models.EmailField(max_length=25)
    phone=models.CharField(max_length=12,null=False, blank=False, unique=True)
    country = models.CharField(max_length=255, default ="")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branch"


class OrganizationSocialChannel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    social_channel = models.ForeignKey(SocialChannel, on_delete=models.CASCADE)
    profile_id  = models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Organization social profile"
        verbose_name_plural = "Organization social profile"



class PlatformCustomerPermissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(PlatformCustomer, on_delete = models.CASCADE)

    class Meta:
        verbose_name = "Customer Permission"
        verbose_name_plural = "Customer Permission"



class FieldType(models.Model):
    icon = models.ImageField(upload_to='field_icons',blank=True, default="", null=True)
    name=models.CharField(max_length=255)     

    def __str__(self):
        return self.name
    

