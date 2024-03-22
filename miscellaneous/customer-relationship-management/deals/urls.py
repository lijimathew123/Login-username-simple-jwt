# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .views import *




urlpatterns = [
   
     path('api/default-deal-fields/', DefaultDealFieldsAPIView.as_view(), name='default-deal-fields'),
     path('api/update-default-deal-fields/', UpdateDefaultFieldView.as_view(), name='update-default-deal-fields'),
     path('api/get-default-deal-status-fields/', DefaultDealStatusAPIView.as_view(), name='default-deal-status-fields'),
     path('api/update-default-deal-status-fields/', UpdateDefaultDealStatusView.as_view(), name='update-default-deal-status-fields'),
     path('api/create-deal/', DealCreateAPIView.as_view(), name='create-deal'),
     path('api/update-deal/', UpdateDealDetailsAPIView.as_view(), name='update-deal'),
     path('api/delete-deal/', DeleteDealAPIView.as_view(), name='delete-deal'),
     path('api/deals-under-organization/', DealByOrganizationAPIView.as_view(), name='deals-under-organization'),
     path('api/get-deal/', DealDetailsAPIView.as_view(), name='get-deal'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)