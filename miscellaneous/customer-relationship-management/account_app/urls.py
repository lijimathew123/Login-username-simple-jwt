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
    SubPlatformUserDeleteView,
    SubPlatformUserListView,
    PlatformUserUpdateView,
    SocialChannelsListAPIView,
    FieldTypeListView,
    LoggedUserOrganizationAPIView
   
   
)


from .views import SendOTPView, VerifyOTPView

from django.contrib.auth import views as auth_views

urlpatterns = [
   
      path('api/customer-types/', CustomerTypeListCreateView.as_view(), name='customer-type-list-create'),
      path('api/platform-customer-registration/', PlatformCustomerCreateView.as_view(), name='platform-customer-registration'),
      path('api/platform-customer-login/', PlatformCustomerLoginView.as_view(), name='login'),
      path('api/platform-customer-update/',PlatformUserUpdateView.as_view, name='platform-cutomer-update'),
      path('api/current-platform-customer/delete/', PlatformCustomerDeleteView.as_view(), name='platform-customer-delete'),
      path('api/platform-customer-details/', PlatformCustomerDetailsCreateView.as_view(), name="platform-customer-details"),

      path('api/register-organization/', OrganizationCreateView.as_view(), name='register-organization'),
      path('api/register-organization-branch/',OrganizationBranchCreateView.as_view(), name='register-organization-branch'),
      path('api/user-details/', LoggedInUserDetailView.as_view(), name='logged-in-user-detail'),
      path('api/logged-in-user/organization/', OrganizationListView.as_view(), name='logged-in-user-organization-detail'),
      path('api/organizations/', OrganizationDetailView.as_view(), name='logged-in-user-organization-branch-detail'),
      path('api/organization-branches/', OrganizationBranchListView.as_view(), name='organization-branch-list'),
      path('api/logout-user/', PlatformCustomerLogoutView.as_view(), name='logout-user'),
     
      path('api/organization-branch/', OrganizationBranchDetailView.as_view(), name='organization-branch-detail'),
      path('api/platform-customer-details-update/', PlatformCustomerDetailsUpdateView.as_view(), name='platform-customer-details-update'),
      path('api/subplatform-users/', SubPlatformUserListView.as_view(), name='subplatform-users-list'),
      path('api/sub-platform-user/<uuid:pk>/update', SubPlatformUserUpdateView.as_view(), name='sub-platform-user-update'),
      path('api/sub-platform-user/<uuid:pk>/delete', SubPlatformUserDeleteView.as_view(), name='sub-platform-user-delete'),
      path('api/send-otp/', SendOTPView.as_view(), name='send-otp'),
      path('api/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
      path('api/social-channels/', SocialChannelsListAPIView.as_view(), name='social-channels-list'),
      path('api/field-types/', FieldTypeListView.as_view(), name='field_types_list'),
      path('api/logged-in-user-organization/', LoggedUserOrganizationAPIView.as_view(), name='logged-in_user_organization'),
     


    #   path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #   path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    #   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    #   path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)