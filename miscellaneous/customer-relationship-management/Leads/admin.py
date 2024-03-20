from django.contrib import admin
from .models import Leads,DefaultLeadCategory,DefaultLeadFields
# Register your models here.

admin.site.register(Leads)
admin.site.register(DefaultLeadCategory)

admin.site.register(DefaultLeadFields)
