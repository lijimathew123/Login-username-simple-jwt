from django.contrib import admin

# Register your models here.
from .models import Role,CustomerRole

admin.site.register(Role)
admin.site.register(CustomerRole)