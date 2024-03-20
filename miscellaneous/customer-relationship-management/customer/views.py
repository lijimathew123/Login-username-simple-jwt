from django.shortcuts import get_object_or_404, render



from .serializers import DefaultCustomerFieldsSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,DefaultCustomerFields
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from bson import ObjectId  
from account_app.models import Organization, PlatformCustomer
from company.models import Company

from account_app.mongo_connection import customer_collection,default_customer_field,company_collection


#    ---------------------- fetch default fields of customer -----------------------   

class DefaultCustomerFieldsAPIView(APIView):
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
            result = default_customer_field.find_one(query)

            # Check if the result exists
            if result:
                # Convert ObjectId to string
                result['_id'] = str(result['_id'])
                return Response(result)
            else:
                return Response({'message': 'No data found for the specified organization_id and Type'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
    


#  ---------------------------  update default fields of customer based on "default_field_id" ------------------------ 
        


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
            result = default_customer_field.update_one(
                {'_id': default_field_id, 'organization_id': organization_id},
                {'$set': {'fields': updated_fields}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Default field updated successfully'})
            else:
                return Response({'message': 'No changes detected'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

    

#   ------------------- All customer under a organization ---------------------  
        
class CustomerByOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            organization_id = request.query_params.get('organization_id')
            if not organization_id:
                return Response({'error': 'organization_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve customer data from MongoDB
            customers_data = customer_collection.find({'organization_id': organization_id})

            response_data = []
            for customer in customers_data:
                response_data.append({
                    'lead_id': customer['lead_id'],
                    'organization_id': customer['organization_id'],
                    'customer_id':customer['customer_id'],

                    'test': customer['test'],
                    # Include additional fields as needed
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



# --------------------- get a customer by customer id ----------------------  
        
# class CustomerDetailsAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             # Get customer_id from query parameters
#             customer_id = request.query_params.get('customer_id')

#             # Check if customer_id is provided
#             if not customer_id:
#                 return Response({'error': 'customer_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

#             # Retrieve customer details from customer_collection
#             customer_data = customer_collection.find_one({'customer_id': customer_id})

#             if customer_data:
#                 # Convert ObjectId to string for _id field
#                 customer_data['_id'] = str(customer_data['_id'])

#                 return Response(customer_data, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get customer_id from query parameters
            customer_id = request.query_params.get('customer_id')
            customer_instance = Customer.objects.get(id=customer_id)

            # Check if customer_id is provided
            if not customer_id:
                return Response({'error': 'customer_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve customer details from customer_collection
            customer_data = customer_collection.find_one({'customer_id': customer_id})

            if customer_data:
                # Convert ObjectId to string for _id field
                customer_data['_id'] = str(customer_data['_id'])

                # Retrieve company details from the MongoDB collection
                company_id = customer_data.get('company_id')
                company_data = company_collection.find_one({'company_id': str(company_id)})  

                # Check if company data exists
                if company_data:
                    company_name = company_data['test'].get('company_name')
                else:
                    company_name = None

                # Retrieve organization details from the PostgreSQL model
                organization_id = customer_data.get('organization_id')
                organization_instance = Organization.objects.get(id=organization_id)
                organization_name = organization_instance.organization_name

                # Retrieve additional data from PlatformCustomer model
                created_by_instance = request.user

                # Include 'lead_id' in the response data if available
                response_data = {
                    '_id': customer_data['_id'],
                    'organization_id': organization_id,
                    'organization_name': organization_name,
                    'customer_id': customer_data['customer_id'],
                    'company_id': company_id,
                    'company_name': company_name,
                    'test': customer_data['test'],
                    'created_by': {
                        'id': created_by_instance.id,
                        'email': created_by_instance.email
                    },
                    'created_at':customer_instance.created_at,
                    'last_modified_at': customer_instance.last_modified_at
                   
                    
                }

                # Check if 'lead_id' exists in customer_data
                if 'lead_id' in customer_data:
                    response_data['lead_id'] = customer_data['lead_id']
                else:
                    response_data['lead_id'] = None  

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#  ------------------------ create a customer from customer module ------------------------   
class CustomerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization_id = request.data.get('organization_id')
        company_id = request.data.get('company_id')
        test_data = request.data.get('test', {})
        
        # Get the current user as the created_by value
        created_by = request.user
        organization_instance = Organization.objects.get(id=organization_id)
        company_instance = Company.objects.get(id = company_id)
        
        try:
            # Create a customer object in the Customer model
            customer = Customer.objects.create(
                organization=organization_instance,
                created_by=created_by,
                created_at=int(timezone.now().timestamp()),
                last_modified_at=int(timezone.now().timestamp()),
                company=company_instance
            )

            
           

            # Store the customer ID in the customer_collection MongoDB collection
            customer_data = {
                'organization_id': organization_id,
                'customer_id': str(customer.id),
                'company_id': company_id,
                'test': test_data
            }
            customer_collection.insert_one(customer_data)

            return Response({'message': 'Customer created successfully', 'customer': str(customer.id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#  ----------------------- Update a customer data --------------------------- 
        

class UpdateCustomerDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            customer_id = data.get('customer_id')
            updated_test_data = data.get('test', {})  # Updated data for the 'test' field
            
            # Retrieve the customer instance from the PostgreSQL Customer model
            customer_instance = Customer.objects.get(id=customer_id)
            
            # Update the last_modified_at field
            customer_instance.last_modified_at = int(timezone.now().timestamp())
            
            # Save the updated customer instance
            customer_instance.save()

            # Update the document in the MongoDB customer_collection
            result = customer_collection.update_one(
                {'customer_id': customer_id},
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
        


#  ----------------------- Delete a customer from mongodb and postgresql ------------------------------------ 
        

class DeleteCustomerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        try:
            # Get customer_id from query parameters
            customer_id = request.query_params.get('customer_id')

            # Check if customer_id is provided
            if not customer_id:
                return Response({'error': 'customer_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the customer from MongoDB
            
            result = customer_collection.delete_one({'customer_id': customer_id})

            # Delete the customer from PostgreSQL
            Customer.objects.filter(id=customer_id).delete()

            if result.deleted_count > 0:
                return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)