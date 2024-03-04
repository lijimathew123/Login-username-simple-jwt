# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
    RoleListCreateView,
    RoleDetailView,
    RoleAssignmentView,
    CustomerRoleDetailView



)


urlpatterns = [
      
     path('api/roles/', RoleListCreateView.as_view(), name='role-list-create'),
     path('api/roles/<int:pk>/',RoleDetailView.as_view(), name='role-detail'),
     path('api/customer-role/<int:organization_id>',RoleAssignmentView.as_view(), name='customer-role-assign'),
     path('api/customer-role/<int:pk>/',CustomerRoleDetailView.as_view(), name='view-customer-role'),

      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)