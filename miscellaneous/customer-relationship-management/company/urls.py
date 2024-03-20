# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
# from .views import OrganizationListView

from .views import *




urlpatterns = [
    
    path('api/default-company-fields/', DefaultCompanyFieldsAPIView.as_view(), name='default-company-fields'),
    path('api/update-default-company-fields/', UpdateDefaultFieldView.as_view(), name='update-default-company-fields'),
    # path('api/organization/',OrganizationListView.as_view(), name=''),
    path('api/company-create/', CompanyCreateAPIView.as_view(), name='company-create'),
    path('api/company-update/', CompanyUpdateAPIView.as_view(), name='company-update'),
    path('api/company-delete/', DeleteCompanyAPIView.as_view(), name='company-delete'),
    path('api/company-under-organization/', CompanyByOrganizationAPIView.as_view(), name='company-under-organization'),
    path('api/get-company/', CompanyDetailsAPIView.as_view(), name='get-company'),
    
  
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)