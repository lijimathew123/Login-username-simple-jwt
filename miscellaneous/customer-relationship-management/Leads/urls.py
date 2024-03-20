# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *


urlpatterns = [
   path('api/get_default_fields/', DefaultFieldListView.as_view(), name='get_default_fields'),
   path('api/update-default-field/', UpdateDefaultFieldView.as_view(), name='update_default_field'),
   path('api/create_lead/', LeadCreateAPIView.as_view(), name='create_lead'),
   path('api/UpdateLeadDataView/',UpdateLeadDataView.as_view(), name='update-lead-data'),
   path('api/leads/', DeleteLeadAPIView.as_view(), name='delete_lead'),
   path('api/get-lead-data/', LeadDetailsAPIView.as_view(), name='get_lead_data'),
   path('api/get-organization-lead/', LeadsByOrganizationAPIView.as_view(), name='get_organization_lead'),
   path('api/get-user-organization/', OwnerAndCustomersListView.as_view(), name='get_user_organization'),

      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)