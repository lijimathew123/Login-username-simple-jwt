from django.contrib import admin
from .models import Customer,DefaultCustomerCategory,DefaultCustomerFields



admin.site.register(Customer)
admin.site.register(DefaultCustomerCategory)
admin.site.register(DefaultCustomerFields)