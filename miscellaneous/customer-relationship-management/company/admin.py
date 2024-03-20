from django.contrib import admin
from .models import Company,DefaultCompanyCategory,DefaultCompanyFields
# Register your models here.
admin.site.register(Company)
admin.site.register(DefaultCompanyCategory)
admin.site.register(DefaultCompanyFields)
