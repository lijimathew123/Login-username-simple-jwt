from django.shortcuts import get_object_or_404, render

# Create your views here.
# views.py




from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee
from .serializers import EmployeeRegistrationSerializer, EmployeeLoginSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView




class EmployeeRegistrationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Employee
from .serializers import EmployeeLoginSerializer

class EmployeeLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmployeeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Retrieve user by username
        user = Employee.objects.filter(username=username).first()

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check password
        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
