from django.urls import path
from .views import EmployeeRegistrationView, EmployeeLoginView

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='employee-register'),
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),
]