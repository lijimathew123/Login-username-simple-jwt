# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *





urlpatterns = [
      path('api/default-customer-fields/', DefaultCustomerFieldsAPIView.as_view(), name='default-customer-fields'),
      path('api/update-default-customer field/', UpdateDefaultFieldView.as_view(), name='update-defult-customer-fields'),
      path('api/get-customers-under-organization/', CustomerByOrganizationAPIView.as_view(), name='get-customers-under-organization'),
      path('api/get-customer/', CustomerDetailsAPIView.as_view(), name='get-customer'),
      path('api/update-customer/', UpdateCustomerDetailsAPIView.as_view(), name='update-customer'),
      path('api/delete-customer/', DeleteCustomerAPIView.as_view(), name='delete-customer'),
      path('api/create-customer/', CustomerCreateAPIView.as_view(), name='create-customer'),

      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)