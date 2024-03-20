from django.contrib import admin
from .models import Deals,DefaultDealStatus,DefaultDealCategory,DefaultDealFields
# Register your models here.

admin.site.register(Deals)

admin.site.register(DefaultDealStatus)

admin.site.register(DefaultDealCategory)

admin.site.register(DefaultDealFields)