from ast import parse
from uuid import uuid4
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
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

from rest_framework import generics


from .models import ( 
    CustomerType,
    PlatformCustomer,
    PlatformCustomerDetails,
    Organization,
    OrganizationBranch,
    UserLastLogin,
    SocialChannel,
    FieldType,
    CustomerOrganization
    
)

from Leads.models import DefaultLeadFields,DefaultLeadCategory
from customer.models import  DefaultCustomerCategory,DefaultCustomerFields
from company.models import DefaultCompanyFields
from deals.models import DefaultDealFields,DefaultDealStatus
from bson import ObjectId


from .serializers import (
    CustomerTypeSerializer,
    PlatformCustomerSerializer,
    PlatformCustomerSerializer,
    PlatfromCustomerDetailsSerializer,
    OrganizationSerializer,
    OrganizationBranchSerializer,
    PlatformCustomerSerializer2,
    SocialChannelSerializer,
    FieldTypeSerializer
    
)



from .mongo_connection import (
    person_collection,
    default_lead_field,
    default_customer_field,
    default_company_field,
    default_deal_field,
    default_deal_status_field
)


# ------------views for save customer types--- (check the needs of creating custom admin module)---------

class CustomerTypeListCreateView(generics.ListCreateAPIView):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer







# ----------views for register platform  customer--------------serializer_class
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
       
        current_user = self.request.user


        #  Get the organization id
        organization_id = self.request.data.get('organization_id')
        print(organization_id)
        
        # Get the customer type ID from the request data
        customer_type_id = self.request.data.get('customer_type')
        print(customer_type_id)
        type_id=customer_type_id['type']

        if customer_type_id:
            try:
                
                customer_type = CustomerType.objects.get(id=type_id)
                
            except CustomerType.DoesNotExist:
                pass  

        # Save the PlatformCustomer object
        if current_user.is_authenticated:
            
               serializer.save(created_by=current_user, customer_type=customer_type,created_at=timezone.now().timestamp())
                    
               if organization_id:
                      organization = Organization.objects.get(id=organization_id)
                      print(organization)
                      if organization:
                          print("organization fount!")
                      CustomerOrganization.objects.create(customer=serializer.instance, organization=organization)



        else:
            # If the user is not logged in, leave created_by as null
            serializer.save(customer_type=customer_type,created_at=timezone.now().timestamp())

            
# ---------------------------views for update platformuser----------------------
            
class  PlatformUserUpdateView(APIView):
    serializer_class = PlatformCustomerSerializer2
    permission_classes=[IsAuthenticated]

    
    
    def patch(self, request, *args, **kwargs):
        email = request.data['email']
        username=request.data['username']
        password=make_password(request.data['password'])
        first_name=request.data['first_name']   
        last_name=request.data['last_name']
        phone=request.data['phone']
       

        try:
            
            obj = self.requset.user
            # Update the fields
            obj.email = email
            obj.first_name = first_name
            obj.last_name = last_name
            obj.phone = phone
            obj.username = username
            obj.password = password
            obj.save()

            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PlatformCustomer.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        



# ---------------------views for platform customer delete view------------------------
class PlatformCustomerDeleteView(generics.DestroyAPIView):
    serializer_class = PlatformCustomerSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
       instance.delete()
       return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# -------------------- social media operation ----------------

class SocialChannelsListAPIView(APIView):
    def get(self, request):
        social_channels = SocialChannel.objects.all()
        serializer = SocialChannelSerializer(social_channels, many=True)
        return Response(serializer.data)



# ----------------------display/update and  delete the  sub-platform user crated by Main platform user----------------
class SubPlatformUserListView(generics.ListAPIView):
    serializer_class = PlatformCustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the organization_id from query parameters
        organization_id = self.request.query_params.get('organization_id')

        # Query CustomerOrganization to filter PlatformCustomer instances associated with the organization
        queryset = PlatformCustomer.objects.filter(customerorganization__organization_id=organization_id)

        return queryset


#  ------------------------ update sub platform customer --------------------

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
    

# ------------------------    delete a subplatform customer ------------------------------
class SubPlatformUserDeleteView(generics.DestroyAPIView):
    serializer_class = PlatformCustomerSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return PlatformCustomer.objects.filter(created_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        try:
            # Ensure the user exists and is a sub-platform user of the current user
            sub_platform_user = self.get_queryset().get(id=user_id)
            sub_platform_user.delete()

            return Response({'message': 'Sub-platform user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except PlatformCustomer.DoesNotExist:
            return Response({'error': 'Sub-platform user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    


# ---------views for platform customer login ---- email and password used for login------------
    
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

            # Update login details in MongoDB for success
            login_document = {
                'user_id': str(user.id),
                'last_login': int(timezone.now().timestamp()),
                'status': "Success",
                'last_login_ip': get_client_ip(request),
            }
            person_collection.insert_one(login_document)
            print("MongoDB login details updated for success")
            
            # Authentication successful
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        else:
            print("Authentication failed!")  

            # Update login details in MongoDB for failure
            login_document = {
                'status': "Failed",
            }
            person_collection.insert_one(login_document)
            print("MongoDB login details updated for failure")
            
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
    


# ----------------view for register organization details(old view) ------------------------
        
# class OrganizationCreateView(generics.CreateAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         # Retrieve the current user from the token
      
#         current_user = request.user

#         # Add the owner (current user) to the request data
#         request.data['owner'] = current_user.id
        
       


#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



from collections import defaultdict


#    ---------------------------use this below view now and  do not delete below view!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -----------------------------------------
class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_user = request.user

        # Add the owner (current user) to the request data
        request.data['owner'] = current_user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        
       
     
              # Handle storing DefaultLeadFields data in MongoDB
        try:
              # Retrieve all instances of DefaultLeadFields
                all_lead_fields = DefaultLeadFields.objects.all()

                # Initialize a dictionary to store categories and their fields
                categories_data = defaultdict(list)

                # Iterate over each lead field instance
                for lead_field in all_lead_fields:
                    # Construct field data
                    field_data = {
                        'id': lead_field.id,
                       
                        'field_type': {
                            'id': lead_field.field_type.id,
                            'name': lead_field.field_type.name
                        },
                        'display_name': lead_field.display_name,
                        'mem_variable': lead_field.mem_variable,
                        'options': lead_field.options,
                        'regex_field': lead_field.regex_field,
                        'required': lead_field.required,
                        'order': lead_field.order,
                        'is_quick': lead_field.is_quick,
                        'is_static': lead_field.is_static
                    }
                    # Append field data to the respective category
                    categories_data[lead_field.catogory.name].append(field_data)

                # Initialize organization_lead_data
                organization_lead_data = {
                    'Type': 'Lead',
                    'organization_id': str(serializer.data['id']),
                    'categories': []
                }

                # Append the categories data to the list
                for category_name, fields in categories_data.items():
                    category_data = {'category_name': category_name, 'fields': fields}
                    organization_lead_data['categories'].append(category_data)

                # Insert the organization's lead data into MongoDB
                default_lead_field.insert_one(organization_lead_data)

        except DefaultLeadFields.DoesNotExist:
            pass
        
             
             # Handle storing DefaultCustomerFields data in MongoDB
        try:
              # Retrieve all instances of DefaultLeadFields
                all_customer_fields = DefaultCustomerFields.objects.all()

                # Initialize a dictionary to store categories and their fields
                categories_data = defaultdict(list)

                # Iterate over each lead field instance
                for customer_field in all_customer_fields:
                    # Construct field data
                    field_data = {
                        'id': customer_field.id,
                       
                        'field_type': {
                            'id': customer_field.field_type.id,
                            'name': customer_field.field_type.name
                        },
                        'display_name': customer_field.display_name,
                        'mem_variable': customer_field.mem_variable,
                        'options': customer_field.options,
                        'regex_field': customer_field.regex_field,
                        'required': customer_field.required,
                        'order': customer_field.order,
                        'is_quick': customer_field.is_quick,
                        'is_static': customer_field.is_static
                    }
                    # Append field data to the respective category
                    categories_data[customer_field.catogory.name].append(field_data)

                # Initialize organization_lead_data
                customer_lead_data = {
                    'Type': 'Customer',
                    'organization_id': str(serializer.data['id']),
                    'categories': []
                }

                # Append the categories data to the list
                for category_name, fields in categories_data.items():
                    category_data = {'category_name': category_name, 'fields': fields}
                    customer_lead_data['categories'].append(category_data)

                # Insert the organization's lead data into MongoDB
                default_customer_field.insert_one(customer_lead_data)

        except DefaultCustomerFields.DoesNotExist:
            pass



        try:
              
                all_company_fields = DefaultCompanyFields.objects.all()

                # Initialize a dictionary to store categories and their fields
                categories_data = defaultdict(list)

                # Iterate over each lead field instance
                for company_field in all_company_fields:
                    # Construct field data
                    field_data = {
                        'id': company_field.id,
                       
                        'field_type': {
                            'id': company_field.field_type.id,
                            'name': company_field.field_type.name
                        },
                        'display_name': company_field.display_name,
                        'mem_variable': company_field.mem_variable,
                        'options': company_field.options,
                        'regex_field': company_field.regex_field,
                        'required': company_field.required,
                        'order': company_field.order,
                        'is_quick': company_field.is_quick,
                        'is_static': company_field.is_static
                    }
                    # Append field data to the respective category
                    categories_data[company_field.catogory.name].append(field_data)

                # Initialize organization_lead_data
                company_field_data = {
                    'Type': 'Customer',
                    'organization_id': str(serializer.data['id']),
                    'categories': []
                }

                # Append the categories data to the list
                for category_name, fields in categories_data.items():
                    category_data = {'category_name': category_name, 'fields': fields}
                    company_field_data['categories'].append(category_data)

                # Insert the organization's lead data into MongoDB
                default_company_field.insert_one(company_field_data)

        except DefaultCompanyFields.DoesNotExist:
            pass



              # Handle storing DefaultDealFields data in MongoDB
        try:
              
                all_deal_fields = DefaultDealFields.objects.all()

                # Initialize a dictionary to store categories and their fields
                categories_data = defaultdict(list)

                # Iterate over each lead field instance
                for deal_field in all_deal_fields:
                    # Construct field data
                    field_data = {
                        'id': company_field.id,
                       
                        'field_type': {
                            'id': deal_field.field_type.id,
                            'name': deal_field.field_type.name
                        },
                        'display_name': deal_field.display_name,
                        'mem_variable': deal_field.mem_variable,
                        'options': deal_field.options,
                        'regex_field': deal_field.regex_field,
                        'required': deal_field.required,
                        'order': deal_field.order,
                        'is_quick': deal_field.is_quick,
                        'is_static': deal_field.is_static
                    }
                    # Append field data to the respective category
                    categories_data[deal_field.catogory.name].append(field_data)

                # Initialize organization_lead_data
                company_field_data = {
                    'Type': 'Deal',
                    'organization_id': str(serializer.data['id']),
                    'categories': []
                }

                # Append the categories data to the list
                for category_name, fields in categories_data.items():
                    category_data = {'category_name': category_name, 'fields': fields}
                    company_field_data['categories'].append(category_data)

                # Insert the organization's lead data into MongoDB
                default_deal_field.insert_one(company_field_data)

        except DefaultCompanyFields.DoesNotExist:
            pass
      
        
        try:
                # Retrieve all instances of DefaultDealStatus
            all_deal_statuses = DefaultDealStatus.objects.all()

            # Initialize a list to store all deal statuses
            deal_statuses = []

            # Iterate over each deal status instance and extract required data
            for deal_status in all_deal_statuses:
                status_data = {
                    'status': deal_status.stage,
                    'probability': deal_status.probability
                }
                deal_statuses.append(status_data)

            # Create a document to store all deal statuses
            deal_status_document = {
                'Type': 'Deal Status',
                'organization_id': str(serializer.data['id']),
                'statuses': deal_statuses
            }

            # Insert the organization's deal statuses into MongoDB
            default_deal_status_field.insert_one(deal_status_document)

        except DefaultDealStatus.DoesNotExist:
            pass







                
        


       

         
       
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)






# ------------------views for display/update all the information of current logged platform user------------
    

class LoggedInUserDetailView(APIView):
    serializer_class = PlatformCustomerSerializer2
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        # Retrieve the logged-in user
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
      
        return Organization.objects.filter(owner=self.request.user)

    def get_object(self):
        # Retrieve organization based on provided ID in the URL
        organization_id = self.request.query_params.get('organization_id')
        try:
            return Organization.objects.get(owner=self.request.user, id=organization_id)
        except Organization.DoesNotExist:
            raise Http404("Organization does not exist for this user.")



# ---------------views for register organization branch details---------------


class OrganizationBranchCreateView(generics.CreateAPIView):
    queryset = OrganizationBranch.objects.all()
    serializer_class = OrganizationBranchSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Extract the organization ID from the request data
        organization_id = request.data.get('organization_id')
        
        if not organization_id:
            return Response({'error': 'Organization ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Add the organization to the request data
        request.data['organization_name'] = organization_id

        # Create the organization branch
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    

    
# ---------------views for displaying list of organization branches of a particular organization

class OrganizationBranchListView(generics.ListAPIView):
    serializer_class = OrganizationBranchSerializer
    queryset = OrganizationBranch.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            return OrganizationBranch.objects.filter(organization_name=organization_id)
        else:
            return OrganizationBranch.objects.none() 

# ----------------display/update/delete  a particular branch------------------
    
class OrganizationBranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationBranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrganizationBranch.objects.all()

    def get_object(self):
        branch_id = self.request.query_params.get('id')
        try:
            return OrganizationBranch.objects.get(id=branch_id)
        except OrganizationBranch.DoesNotExist:
            return Response({'error': 'Organization branch not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------View for logout---------------------------   

class PlatformCustomerLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({'message':'Logout Successfully'}, status=status.HTTP_200_OK)
    




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



class FieldTypeListView(APIView):
    def get(self, request):
      
        field_types = FieldType.objects.all()
        serializer = FieldTypeSerializer(field_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




#  ------------------------ view for get details of organization of current logged in user ------------------------
    
class LoggedUserOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get the current logged-in user
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the organization details associated with the user
        if user.platform_customer_owner.exists():
            organizations = Organization.objects.filter(owner=user)
        else:
            organizations = Organization.objects.filter(customerorganization__customer=user)

        # Serialize the organization details
        serializer = OrganizationSerializer(organizations, many=True)

        return Response({'organizations': serializer.data}, status=status.HTTP_200_OK)