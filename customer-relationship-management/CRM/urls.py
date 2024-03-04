
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('accounts/',include('account_app.urls')),
    path('leads/',include('Leads.urls')),
    
    path('api-auth/', include('rest_framework.urls')),
    
   
]
