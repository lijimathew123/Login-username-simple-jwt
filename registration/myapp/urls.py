from django.urls import path
from .views import EmployeeRegistrationView,EmployeeLoginAPIView


urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='employee-register'),
    
    path('api/token/', EmployeeLoginAPIView.as_view(), name='token_obtain_pair'),
   
]
