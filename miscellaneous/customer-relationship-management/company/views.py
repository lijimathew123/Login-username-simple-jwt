from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Company,DefaultCompanyFields
from .serializers import (
  CompanySerializer,
  DefaultCompanyFieldsSerializer,
  OrganizationSerializer
) 

from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import datetime
import uuid

from account_app.models import *
from customer.models import *

from account_app.mongo_connection import db 
from account_app.mongo_connection import default_company_field,company_collection


from bson import ObjectId  

# ---------------------------- get default company fields --------------------------


class DefaultCompanyFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve query parameters
            organization_id = request.query_params.get('organization_id')
            lead_type = request.query_params.get('Type')

            # Query MongoDB collection based on organization_id and Type
            query = {
                'organization_id': organization_id,
                'Type': lead_type
            }
            result = default_company_field.find_one(query)

            # Check if the result exists
            if result:
                # Convert ObjectId to string
                result['_id'] = str(result['_id'])
                return Response(result)
            else:
                return Response({'message': 'No data found for the specified organization_id and Type'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
    


# -------------------------  Update default company fields ----------------------------------------
        
class UpdateDefaultFieldView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            default_field_id = data.get('default_field_id')
            updated_fields = data.get('fields')
            organization_id = data.get('organization_id')

            

            # Convert default_field_id to ObjectId
            default_field_id = ObjectId(default_field_id)

            # Update the document in MongoDB
            result = default_company_field.update_one(
                {'_id': default_field_id, 'organization_id': organization_id},
                {'$set': {'fields': updated_fields}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Default field updated successfully'})
            else:
                return Response({'message': 'No changes detected'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)





# -----------------------------get list of organization----------------
# class OrganizationListView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         current_user = request.user
#         organizations = Organization.objects.filter(owner=current_user)
#         serializer = OrganizationSerializer(organizations, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    




#  --------------------------- create a company and store in postgresql and mongodb -----------------------------
    
class CompanyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization_id = request.data.get('organization_id')
        test_data = request.data.get('test', {})
        
        # Get the current user as the created_by value
        created_by = request.user
        
        try:
            company = Company.objects.create(
                organization_id=organization_id,
                created_by=created_by,
                created_at=int(timezone.now().timestamp()),
                last_modified_at=int(timezone.now().timestamp()),
            )

            # Store the customer ID in the company collection
            company_data = {
                'organization_id': organization_id,
                'company_id': str(company.id),
                'test': test_data
            }
            company_collection.insert_one(company_data)

            return Response({'message': 'Company created successfully', 'company_id': str(company.id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        




#  --------------------- update company details --------------------------
        
class CompanyUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            company_id = data.get('company_id')
            updated_test_data = data.get('test', {})  # Updated data for the 'test' field
            
            # Retrieve the customer instance from the PostgreSQL Customer model
            customer_instance = Company.objects.get(id=company_id)
            
            # Update the last_modified_at field
            customer_instance.last_modified_at = int(timezone.now().timestamp())
            
            # Save the updated customer instance
            customer_instance.save()

            # Update the document in the MongoDB customer_collection
            result = company_collection.update_one(
                {'company_id': company_id},
                {'$set': {'test': updated_test_data}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Customer details updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No changes detected'}, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

# ----------------------------- delete a company details from postgresql and mongodb  --------------------
        
class DeleteCompanyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        try:
            # Get customer_id from query parameters
            company_id = request.query_params.get('company_id')

            # Check if customer_id is provided
            if not company_id:
                return Response({'error': 'customer_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the customer from MongoDB
            
            result = company_collection.delete_one({'company_id': company_id})

            # Delete the customer from PostgreSQL
            Company.objects.filter(id=company_id).delete()

            if result.deleted_count > 0:
                return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      
        


#  ---------------------- all company under a organization ---------------------------- 
        
class CompanyByOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            organization_id = request.query_params.get('organization_id')
            if not organization_id:
                return Response({'error': 'organization_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve company data from MongoDB
            companies_data = company_collection.find({'organization_id': organization_id})

            response_data = []
            for company in companies_data:
                response_data.append({
                    'organization_id': company['organization_id'],
                    'company_id_id': company['company_id'],
                    'test': company['test'],
                    
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        




#    ------------------------- get a company details ----------------------------------

class CompanyDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get company_id from query parameters
            company_id = request.query_params.get('company_id')

            # Check if company_id is provided
            if not company_id:
                return Response({'error': 'company_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve company details from company_collection
            company_data = company_collection.find_one({'company_id': company_id})

            if company_data:
                # Convert ObjectId to string if needed
                company_data['_id'] = str(company_data['_id'])

                # Retrieve additional data from Company model
                company_instance = get_object_or_404(Company, pk=company_id)
                created_by = {
                    'id': company_instance.created_by.id,
                    'email': company_instance.created_by.email
                }
                created_at = company_instance.created_at
                last_modified_at = company_instance.last_modified_at

                # Include additional data in the response
                company_data['created_by'] = created_by
                company_data['created_at'] = created_at
                company_data['last_modified_at'] = last_modified_at

                return Response(company_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

