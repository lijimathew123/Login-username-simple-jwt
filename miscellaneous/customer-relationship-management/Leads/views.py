
from django.db.models import Q


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# from .serializers import




from account_app.models import *

from account_app.mongo_connection import db 

from account_app.mongo_connection import default_lead_field,leads_collection,customer_collection,company_collection
from .models import Leads
from company.models import Company
from customer.models import Customer, DefaultCustomerFields

     

# ------------ Get default leads list from mongoDB -------------------------

from bson import ObjectId  

class DefaultFieldListView(APIView):
    # permission_classes = [IsAuthenticated]
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
            result = default_lead_field.find_one(query)

            # Check if the result exists
            if result:
                # Convert ObjectId to string
                result['_id'] = str(result['_id'])
                return Response(result)
            else:
                return Response({'message': 'No data found for the specified organization_id and Type'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        


#  ------------------- Update default Lead  fields --------------------------- 


class UpdateDefaultFieldView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            default_field_id = data.get('default_field_id')
            updated_fields = data.get('fields')
            organization_id = data.get('organization_id')

            # Connect to MongoDB
           

            # Convert default_field_id to ObjectId
            default_field_id = ObjectId(default_field_id)

            # Update the document in MongoDB
            result = default_lead_field.update_one(
                {'_id': default_field_id, 'organization_id': organization_id},
                {'$set': {'fields': updated_fields}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Default field updated successfully'})
            else:
                return Response({'message': 'No changes detected'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)



#  --------------------- view for owner and associated platform customer of a organization for drop down --------------
        
class OwnerAndCustomersListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get the organization ID from query parameters
        organization_id = request.query_params.get('organization_id')

        # Retrieve the organization instance or return 404 if not found
        organization = get_object_or_404(Organization, id=organization_id)

        # Retrieve the owner of the organization
        owner = organization.owner

        # Retrieve associated platform customers
        associated_customers = PlatformCustomer.objects.filter(customerorganization__organization=organization)

        # Serialize the data
        owner_data = {
            'id': owner.id,
            'username': owner.username,
            # Add other owner fields here if needed
        }

        customers_data = [
            {
                'id': customer.id,
                'username': customer.username,
                # Add other customer fields here if needed
            }
            for customer in associated_customers
        ]

        return Response({
            'owner': owner_data,
            'associated_customers': customers_data
        })       

#  --------------------- Create new Lead ----------------------------- 



class LeadCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.get('data', {})
            test_data = data.get('test', {})
            organization_id = data.get('organization_id')
            company_id = data.get('company_id')
            organization_instance = Organization.objects.get(id=organization_id)
            company_instance = Company.objects.get(id=company_id)
            created_by = request.user
            created_at = int(timezone.now().timestamp())
            last_modified_at = created_at

            # Create a Lead object in PostgreSQL
            lead = Leads.objects.create(
                organization=organization_instance,
                created_by=created_by,
                created_at=created_at,
                last_modified_at=last_modified_at,
                company=company_instance
            )

            lead_id = str(lead.id)

            # Save the Lead data to MongoDB
            leads_collection.insert_one({'lead_id': lead_id, 'organization_id': organization_id, 'company_id': company_id, 'test': test_data})

            if test_data.get('converted_to_customer', False):
                # Get data from leads_collection
                lead_data = leads_collection.find_one({'lead_id': lead_id})

                # Create a Customer object
                customer = Customer.objects.create(
                    organization=organization_instance,
                    created_by=created_by,
                    last_modified_at=last_modified_at,
                    company=company_instance
                )

                customer.save()

                default_customer_fields = DefaultCustomerFields.objects.all().values_list('mem_variable', flat=True)
                filtered_test_data = {key: value for key, value in test_data.items() if key in default_customer_fields}

                # Move lead data to customer_collection
                customer_data = {
                    'lead_id': lead_data['lead_id'],
                    'organization_id': lead_data['organization_id'],
                    'customer_id': str(customer.id),
                    'company_id': company_id,
                    'test': filtered_test_data
                }

                # Save customer data to customer_collection
                customer_collection.insert_one(customer_data)

            return Response({'message': 'Data saved to PostgreSQL and MongoDB successfully', 'lead_id': lead_id}, status=status.HTTP_201_CREATED)

        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#  ------------------ view Leads under a Organization ------------------
class LeadsByOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            organization_id = request.query_params.get('organization_id')
            if not organization_id:
                return Response({'error': 'organization_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            leads_data = leads_collection.find({'organization_id': organization_id})

            response_data = []
            for lead in leads_data:
                if 'test' in lead:  # Check if the 'test' key is present in the lead data
                    response_data.append({
                        'lead_id': lead['lead_id'],
                        'organization_id': lead['organization_id'],
                        'test': lead['test']
                    })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




#  ----------------------- View a lead --------------------- 





class LeadDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get lead_id from query parameters
            lead_id = request.query_params.get('lead_id')

            # Check if lead_id is provided
            if not lead_id:
                return Response({'error': 'lead_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve lead details from MongoDB
            lead_data = leads_collection.find_one({'lead_id': lead_id})

            if lead_data is None:
                return Response({'error': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve lead details from PostgreSQL
            lead_instance = Leads.objects.get(id=lead_id)

            # Retrieve the name and ID of the person who created the lead
            created_by_instance = lead_instance.created_by
            created_by_name = created_by_instance.get_full_name() if created_by_instance else None
            created_by_id = created_by_instance.id if created_by_instance else None

            # Retrieve the name and ID of the company associated with the lead
            company_instance = lead_instance.company
            company_name = None
            company_id = None
            if company_instance:
                company_data = company_collection.find_one({'company_id': str(company_instance.id)})
                if company_data:
                    company_name = company_data['test'].get('company_name')
                    company_id = company_instance.id

            # Construct response data
            response_data = {
                'lead_id': lead_id,
                'organization_id': lead_data.get('organization_id'),
                'created_by_id': created_by_id,
                'created_by_name': created_by_name,
                'created_at': lead_instance.created_at,
                'last_modified_at': lead_instance.last_modified_at,
                'company_id': company_id,
                'company_name': company_name,
                'test': lead_data.get('test')
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Leads.DoesNotExist:
            return Response({'error': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#  -------------------- Update current lead ----------------------------


class UpdateLeadDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            lead_id = data.get('lead_id')
            updated_data = data.get('test', {})  # Updated data for the 'test' field
            converted_to_customer = updated_data.get('converted_to_customer', False)  # Retrieve from 'test' data
            company_id = data.get('company_id') 
            org_id = data.get('organization_id')
            
            # Convert lead_id to string
            lead_id = str(lead_id)
            
            # Update last_modified_at and converted_to_customer fields in Leads model
            lead_instance = Leads.objects.get(id=lead_id)
            lead_instance.last_modified_at = int(timezone.now().timestamp())
            lead_instance.converted_to_customer = converted_to_customer 

            company_instance = Company.objects.get(id=company_id)
            lead_instance.company = company_instance
            lead_instance.save()

            # Check if converted_to_customer is True
            if converted_to_customer:
                # Get data from leads_collection
                lead_data = leads_collection.find_one({'lead_id': lead_id})
                
                # Create a Customer object
                customer = Customer.objects.create(
                    organization=lead_instance.organization,
                    created_by=lead_instance.created_by,
                    last_modified_at=lead_instance.last_modified_at,
                    company=company_instance
                )
             
                customer.save()

                # Filter test data based on DefaultCustomerFields
                default_customer_fields = DefaultCustomerFields.objects.all().values_list('mem_variable', flat=True)
                filtered_test_data = {key: value for key, value in lead_data['test'].items() if key in default_customer_fields}
                

                # Move lead data to customer_collection
                customer_data = {
                    'lead_id': lead_data['lead_id'],
                    'organization_id': lead_data['organization_id'],
                    'customer_id': str(customer.id),
                    'company_id':company_id,
                    'test': filtered_test_data
                   
                }
                
                customer_collection.insert_one(customer_data)

            else:
                # If converted_to_customer is False, delete the customer from MongoDB collection and Customer model
                lead_data = leads_collection.find_one({'lead_id': lead_id})
                if lead_data:
                    # Filter Customer objects based on the associated organization
                    Customer.objects.filter(organization=lead_instance.organization).delete()
                    # Remove the lead data from the customer_collection
                    customer_collection.delete_one({'organization_id': org_id, 'lead_id': lead_id,})
            
           
                    
            
            # Update the document in MongoDB
            result = leads_collection.update_one(
                {'lead_id': lead_id},
                {'$set': {'test': updated_data, 'converted_to_customer': converted_to_customer}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Lead data updated successfully'})
            else:
                return Response({'message': 'No changes detected'}, status=status.HTTP_200_OK)

        except Leads.DoesNotExist:
            return Response({'error': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#  ----------------------- Delete a Lead -------------------------------- 
        
class DeleteLeadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        try:
            # Get the lead_id from the URL parameters
            lead_id = request.query_params.get('lead_id')

            if not lead_id:
                return Response({'error': 'Lead ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        
         
            # Convert lead_id to ObjectId
            lead_id = str(lead_id)

            # Delete the lead document from MongoDB
            result = leads_collection.delete_one({'lead_id': lead_id})

            lead_instance = Leads.objects.get(id=lead_id)
            lead_instance.delete()

            # Check if the lead was successfully deleted
            if result.deleted_count == 1:
                return Response({'message': 'Lead deleted successfully'})
            else:
                return Response({'message': 'Lead not found'}, status=404)

        except Leads.DoesNotExist:
            return Response({'error': 'Lead not found in Django model'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)