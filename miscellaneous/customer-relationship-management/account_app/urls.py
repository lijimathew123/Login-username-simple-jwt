# urls.py
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static



from .views import (
    CustomerTypeListCreateView, 
    PlatformCustomerCreateView,
    PlatformCustomerLoginView,
    PlatformCustomerDetailsCreateView,
    OrganizationBranchCreateView,
    OrganizationCreateView,
    LoggedInUserDetailView,
    PlatformCustomerDetailsUpdateView,
    OrganizationListView,
    OrganizationDetailView,
    OrganizationBranchListView,
    PlatformCustomerLogoutView,
    PlatformCustomerDeleteView,
    OrganizationBranchDetailView,
    SubPlatformUserUpdateView,
    SubPlatformUserDeleteView
)


from .views import SendOTPView, VerifyOTPView

urlpatterns = [
      path('api/customer-types/', CustomerTypeListCreateView.as_view(), name='customer-type-list-create'),
      path('api/platform-customer-registration/', PlatformCustomerCreateView.as_view(), name='platform-customer-registration'),
      path('api/platform-customer-login/', PlatformCustomerLoginView.as_view(), name='login'),
      path('api/platform-customer-details/', PlatformCustomerDetailsCreateView.as_view(), name="platform-customer-details"),

      path('api/register-organization/', OrganizationCreateView.as_view(), name='register-organization'),
      path('api/register-organization-branch/',OrganizationBranchCreateView.as_view(), name='register-organization-branch'),
      path('api/user-details/', LoggedInUserDetailView.as_view(), name='logged-in-user-detail'),
      path('api/logged-in-user/organization/', OrganizationListView.as_view(), name='logged-in-user-organization-detail'),
      path('api/organizations/<int:pk>/', OrganizationDetailView.as_view(), name='logged-in-user-organization-branch-detail'),
      path('api/organization-branches/<int:organization_id>/', OrganizationBranchListView.as_view(), name='organization-branch-list'),
      path('api/logout-user/', PlatformCustomerLogoutView.as_view(), name='logout-user'),
      path('api/platform-customer/delete/<int:pk>/', PlatformCustomerDeleteView.as_view(), name='platform-customer-delete'),
      path('api/organization/<int:organization_id>/branch/<int:pk>/', OrganizationBranchDetailView.as_view(), name='organization-branch-detail'),
      path('api/platform-customer-details-update/', PlatformCustomerDetailsUpdateView.as_view(), name='platform-customer-details-update'),
      path('api/sub-platform-user/<int:pk>/update', SubPlatformUserUpdateView.as_view(), name='sub-platform-user-update'),
      path('api/sub-platform-user/<int:pk>/delete', SubPlatformUserDeleteView.as_view(), name='sub-platform-user-delete'),
      path('api/send-otp/', SendOTPView.as_view(), name='send-otp'),
      path('api/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)