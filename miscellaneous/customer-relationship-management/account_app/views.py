from ast import parse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from rest_framework.views import APIView

from django.core.signing import loads
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.http import Http404
from django.shortcuts import get_object_or_404



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate







# Create your views here.


from rest_framework import generics

from .models import CustomerType, PlatformCustomer,PlatformCustomerDetails,Organization,OrganizationBranch
from .serializers import (
    CustomerTypeSerializer,
    PlatformCustomerSerializer,
    PlatformCustomerSerializer,
    PlatfromCustomerDetailsSerializer,
    OrganizationSerializer,
    OrganizationBranchSerializer,
    PlatformCustomerSerializer2
)

# ------------views for save customer types--- (check the needs of creating custome admin module)---------

class CustomerTypeListCreateView(generics.ListCreateAPIView):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer





from django.contrib.auth.hashers import make_password
# ----------views for register platform  customer--------------
class PlatformCustomerCreateView(generics.CreateAPIView):
    queryset = PlatformCustomer.objects.all()
    serializer_class = PlatformCustomerSerializer


    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        print("--------------------------------")
        print(serializer)
        print("--------------------------------")
        # Check if the registration is done by the user or by someone else
        if self.request.user.is_authenticated:

            # If the user is logged in, set created_by to the logged-in user

            serializer.save(created_by=self.request.user)
        else:
            # If the user is not logged in, leave created_by as null
            serializer.save()



        

        # return Response(serializer.data, status=status.HTTP_201_CREATED)



# --------------------display/update or delete the  sub-platform user crated by Main platform user----------------
from django.contrib.auth.hashers import make_password
class  SubPlatformUserUpdateView(APIView):
    serializer_class = PlatformCustomerSerializer2
    permission_classes=[IsAuthenticated]

    
    
    def patch(self, request, *args, **kwargs):
        email = request.data['email']
        username=request.data['username']
        password=make_password(request.data['password'])
       
        first_name=request.data['first_name']   
        last_name=request.data['last_name']
        phone=request.data['phone']
        user_id = kwargs.get('pk')

        # Check if 'id' is provided
        if user_id is None:
            return Response({'error': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the PlatformCustomer instance
            obj = PlatformCustomer.objects.get(id=user_id)

            # Update the fields
            obj.email = email
            obj.first_name = first_name
            obj.last_name = last_name
            obj.phone = phone
            obj.username = username
            obj.password = password
            obj.save()

            # Create the serializer with the updated instance
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            
            # Validate and save the serializer
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PlatformCustomer.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

class SubPlatformUserDeleteView(generics.DestroyAPIView):
    serializer_class = PlatformCustomerSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return PlatformCustomer.objects.filter(created_by=self.request.user)
    
    


# ---------views for platform customer login ----email and password used for login------------
    

from helper.authentication import EmailBackend

class PlatformCustomerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"1{email}1 1{password}1")
        
        print(f"Attempting login with email: {email} and password: {password}")

        user = EmailBackend.authenticate(self, request, username=email, password=password)

        print(user)
        if user is not None:
            print("User successfully authenticated!") 
            user.update_last_login() 
            user.update_last_login(ip_address=get_client_ip(request))
            print("reached the login")
            # Authentication successful
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        else:
            # Authentication failed
            print("Authentication failed!")  # Add this line
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ------function for get client ip address------------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



# --------view for add extra details of platform customer after login-----------
class PlatformCustomerDetailsCreateView(generics.CreateAPIView):
    queryset = PlatformCustomerDetails.objects.all()
    serializer_class = PlatfromCustomerDetailsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print(request.user.id)
        request.data['customer']= self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
# ----view for update extra details of platform customer----------------
class PlatformCustomerDetailsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PlatformCustomerDetails.objects.all()
    serializer_class = PlatfromCustomerDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return PlatformCustomerDetails.objects.filter(customer=self.request.user.id).first()
        except PlatformCustomerDetails.DoesNotExist:
            raise Http404("PlatformCustomerDetails does not exist for this user.")
    



# ----------------view for register organization details ------------------------
class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Retrieve the current user from the token
        current_user = request.user

        # Add the owner (current user) to the request data
        request.data['owner'] = current_user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# ---------------views for register organization branch details---------------

class OrganizationBranchCreateView(generics.CreateAPIView):
    queryset = OrganizationBranch.objects.all()
    serializer_class = OrganizationBranchSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Retrieve the current user from the token
        current_user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


# ------------------views for display/update all the information of current logged platform user------------
    
from . serializers import PlatformCustomerSerializer2
class LoggedInUserDetailView(APIView):
    serializer_class = PlatformCustomerSerializer2
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        email = request.data['email']
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        phone=request.data['phone']
        obj = PlatformCustomer.objects.get(id = request.data['id'])
        obj.email = email
        obj.first_name = first_name
        obj.last_name = last_name
        obj.phone = phone


        obj.save()
        instance = obj
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# ------------views  for displaying all organization list off logged user--------------
class OrganizationListView(generics.ListAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve organizations of the logged-in user
        return Organization.objects.filter(owner=self.request.user)
    

    
# ----------------views for displaying/update/delete a perticular  organization details------------
class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve organizations of the logged-in user
        return Organization.objects.filter(owner=self.request.user)
    


    
# ---------------views for displaying list of organization branches of a particular organization

class OrganizationBranchListView(generics.ListAPIView):
    serializer_class = OrganizationBranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve organization branches of the logged-in user
        organization_id = self.kwargs.get('organization_id')
        return OrganizationBranch.objects.filter(organization_name__owner=self.request.user, organization_name__id=organization_id)


# ----------------display  a particular branch------------------
    
class OrganizationBranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationBranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        # Retrieve organization branches of the logged-in user and for a specific organization
        return OrganizationBranch.objects.filter(organization_name__owner=self.request.user, organization_name_id=organization_id)


# --------------View for logout---------------------------   

from django.contrib.auth import logout

class PlatformCustomerLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({'message':'Logout Successfully'}, status=status.HTTP_200_OK)
    


# -------views for platform customer delete view------------------------
class PlatformCustomerDeleteView(generics.DestroyAPIView):
    queryset = PlatformCustomer.objects.all()
    serializer_class = PlatformCustomerSerializer
    permission_classes = [IsAuthenticated]



# -------------------views  for OTP SEND and Verification---------------

import phonenumbers
import random
from .models import OTP
from phonenumbers import PhoneNumberFormat
import requests

class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed_number = parse(phone_number, None)
            phone_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
        except phonenumbers.NumberFormatException:
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        otp_value = str(random.randint(100000, 999999))

        OTP.objects.filter(phone_number=phone_number).delete()  # Remove previous OTPs
        OTP.objects.create(phone_number=phone_number, otp_value=otp_value)

        # Use 2Factor API to send OTP
        api_key = '0490e129-d6df-11ee-8cbb-0200cd936042'
        response = requests.get(
            f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp_value}/YourAppName'
        )

        if response.json()['Status'] != 'Success':
            return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


from phonenumbers import parse, PhoneNumberFormat
class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp_value = request.data.get('otp_value')

        if not phone_number or not otp_value:
            return Response({'error': 'Phone number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed_number = parse(phone_number, None)
            phone_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
        except phonenumbers.NumberFormatException:
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        # Use 2Factor API to verify OTP
        # api_key = '0490e129-d6df-11ee-8cbb-0200cd936042'
        # response = requests.get(
        #     f'https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{phone_number}/{otp_value}'
        # )

        try: 
            user = get_object_or_404(PlatformCustomer, phone=phone_number)
            generated_otp = OTP.objects.get(phone_number=phone_number)

            print("start{}end".format(generated_otp.otp_value))
            print("start{}end".format(generated_otp.phone_number))
            print("start{}end".format(generated_otp.otp_value))
            
            if generated_otp.otp_value == otp_value:
                user = PlatformCustomer.objects.get(phone=phone_number)
                user.verify_phone()
                return Response({'message': 'OTP verification successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({'error':'User not found with this phone number'},status=status.HTTP_404_NOT_FOUND)
