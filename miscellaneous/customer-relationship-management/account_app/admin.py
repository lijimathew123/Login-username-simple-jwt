from django.contrib import admin
from .models import (
  CustomerType,
  PlatformCustomer,
  PlatformCustomerDetails,
  Organization,
  OrganizationBranch,
  Theme,
  SocialChannel,
  PlatformCustomerSocialChannels,
  OrganizationSocialChannel,
  FieldType
) 
# Register your models here.
admin.site.register(CustomerType)
admin.site.register(PlatformCustomer)
admin.site.register(PlatformCustomerDetails)
admin.site.register(Organization)
admin.site.register(OrganizationBranch)
admin.site.register(Theme)
admin.site.register(SocialChannel)
admin.site.register(PlatformCustomerSocialChannels)
admin.site.register(OrganizationSocialChannel)
admin.site.register(FieldType)