# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .views import *




urlpatterns = [
   
     path('api/default-deal-fields/', DefaultDealFieldsAPIView.as_view(), name='default-deal-fields'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)