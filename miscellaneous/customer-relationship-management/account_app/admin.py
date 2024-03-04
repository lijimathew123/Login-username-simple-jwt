from django.contrib import admin
from .models import CustomerType,PlatformCustomer,PlatformCustomerDetails,Organization,OrganizationBranch
# Register your models here.
admin.site.register(CustomerType)
admin.site.register(PlatformCustomer)
admin.site.register(PlatformCustomerDetails)
admin.site.register(Organization)
admin.site.register(OrganizationBranch)