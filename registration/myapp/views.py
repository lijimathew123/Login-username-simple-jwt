from django.shortcuts import get_object_or_404, render

# Create your views here.
# views.py




from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee
from .serializers import EmployeeRegistrationSerializer, EmployeeLoginSerializer
from django.contrib.auth.hashers import check_password




class EmployeeRegistrationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegistrationSerializer
    permission_classes = (permissions.AllowAny,)






class EmployeeLoginView(generics.CreateAPIView):
   
    serializer_class = EmployeeLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = get_object_or_404(Employee, email=email)

        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })