from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role, CustomerRole 
from account_app.models import PlatformCustomer,Organization
from account_app.serializers import PlatformCustomerSerializer
from django.db.models import Q

from .serializers import (
    RoleSerializer,
    CustomerRoleSerializer
    )


#------------ views for create and list roles------------------------

class RoleListCreateView(APIView):
    def get(self, request):
        # Retrieve the organizations owned by the logged-in user
        organizations = Organization.objects.filter(owner=request.user)
        
        # Get roles for the organizations owned by the user
        roles = Role.objects.filter(organization__in=organizations)
        
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Retrieve the organizations owned by the logged-in user
        organizations = Organization.objects.filter(owner=request.user)
        
        # Check if the user owns any organization
        if not organizations.exists():
            return Response({'error': 'User does not own any organization'}, status=status.HTTP_400_BAD_REQUEST)
        
        # If the customer selected an organization in the request data, use that organization
        organization_id = request.data.get('organization')
        if organization_id:
            try:
                organization = organizations.get(id=organization_id)
            except Organization.DoesNotExist:
                return Response({'error': 'Invalid organization ID'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Use the first organization owned by the user as a default
            organization = organizations.first()

        # Create a mutable copy of request.data
        mutable_request_data = request.data.copy()
        
        # Add the chosen organization to the mutable copy
        mutable_request_data['organization'] = organization.id

        serializer = RoleSerializer(data=mutable_request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------views for retrieving updating and delete the Roles list --------------------
class RoleDetailView(APIView):
    def get(self,request,pk):
        role = Role.objects.get(pk=pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        role = Role.objects.get(pk=pk)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        role=Role.objects.get(pk=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------views for assign roles to customer/ display ----------
class RoleAssignmentView(APIView):
    def get(self, request, organization_id):
        # Ensure that the organization exists
        try:
            organization = Organization.objects.get(id=organization_id, owner=request.user)
        except Organization.DoesNotExist:
            return Response({'error': 'Invalid organization ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve roles for the selected organization
        roles = Role.objects.filter(organization=organization)
        role_serializer = RoleSerializer(roles, many=True)

        # Retrieve customers added by the current logged-in user
        customers = PlatformCustomer.objects.filter(created_by=request.user)
        customer_serializer = PlatformCustomerSerializer(customers, many=True)

        # Include both role and customer lists in the response
        response_data = {
            'roles': role_serializer.data,
            'customers': customer_serializer.data,
        }

        return Response(response_data)

    def post(self, request, organization_id):
        # Ensure that the organization exists
        try:
            organization = Organization.objects.get(id=organization_id, owner=request.user)
        except Organization.DoesNotExist:
            return Response({'error': 'Invalid organization ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Deserialize customer roles from the request data
        serializer = CustomerRoleSerializer(data=request.data, many=True, context={'organization': organization})
        if serializer.is_valid():
            # Save the customer roles
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------view roles of a customer/edit roles of customer/ delete roles of customer
        
class CustomerRoleDetailView(APIView):
    def get(self,request,pk):
        customer_role = CustomerRole.objects.get(pk=pk)
        serializer = CustomerRoleSerializer(customer_role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,pk):
        customer_role=CustomerRole.objects.get(pk=pk)
        serializer = CustomerRoleSerializer(customer_role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        customer_role=CustomerRole.objects.get(pk=pk)
        customer_role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

  
