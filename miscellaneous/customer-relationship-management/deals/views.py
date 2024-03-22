
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account_app.models import Organization
from .models import DefaultDealFields,Deals
from rest_framework.permissions import IsAuthenticated
from .serializers import DefaultDealFieldsSerializer
from bson import ObjectId  
from django.utils import timezone

from account_app.mongo_connection import default_deal_field,deal_collection,default_deal_status_field



#   --------------------------- get default deal fields --------------------- 

class DefaultDealFieldsAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve query parameters
            organization_id = request.query_params.get('organization_id')
            type = request.query_params.get('Type')

            # Query MongoDB collection based on organization_id and Type
            query = {
                'organization_id': organization_id,
                'Type': type
            }
            result = default_deal_field.find_one(query)

            # Check if the result exists
            if result:
                # Convert ObjectId to string
                result['_id'] = str(result['_id'])
                
                # Transform the result to match the desired response structure
                transformed_result = {
                    "_id": result["_id"],
                    "Type": result["Type"],
                    "organization_id": result["organization_id"],
                    "categories": []
                }
                
                # Iterate over categories in the original result
                for category in result["categories"]:
                    # Create a new category dictionary
                    new_category = {
                        "category_name": category["category_name"],
                        "fields": category["fields"]
                    }
                    # Append the new category to the transformed result
                    transformed_result["categories"].append(new_category)

                return Response(transformed_result)
            else:
                return Response({'message': 'No data found for the specified organization_id and Type'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        


# -------------------------  Update default deal fields ----------------------------------------
        

class UpdateDefaultFieldView(APIView):
    # permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            default_field_id = data.get('default_field_id')
            updated_fields = data.get('categories')
            organization_id = data.get('organization_id')

            # Convert default_field_id to ObjectId
            default_field_id = ObjectId(default_field_id)

            # Update the document in MongoDB
            result = default_deal_field.update_one(
                {'_id': default_field_id, 'organization_id': organization_id},
                {'$set': {'categories': updated_fields}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Default field updated successfully'})
            else:
                return Response({'message': 'No changes detected'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

    

#    ---------------------------- get  default deal status field ---------------------- 
        
class DefaultDealStatusAPIView(APIView):
  # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve query parameters
            organization_id = request.query_params.get('organization_id')
            type = request.query_params.get('Type')

            # Connect to MongoDB
          

            # Query MongoDB collection based on organization_id and Type
            query = {
                'organization_id': organization_id,
                'Type': type
            }
            result = default_deal_status_field.find_one(query)

            # Check if the result exists
            if result:
                # Convert ObjectId to string
                result['_id'] = str(result['_id'])
                return Response(result)
            else:
                return Response({'message': 'No data found for the specified organization_id and Type'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)       

#    -------------------------- update default deal status field -----------------------  
        
class UpdateDefaultDealStatusView(APIView):
    # permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            default_field_id = data.get('default_field_id')
            updated_statuses = data.get('statuses')
            organization_id = data.get('organization_id')

            # Convert default_field_id to ObjectId
            default_field_id = ObjectId(default_field_id)

            # Connect to MongoDB
         

            # Update the document in MongoDB
            result = default_deal_status_field.update_one(
                {'_id': default_field_id, 'organization_id': organization_id},
                {'$set': {'statuses': updated_statuses}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Default deal status updated successfully'})
            else:
                return Response({'message': 'No changes detected'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

#  ----------------- create a Deal from Deal module  ----------------------------------- 
        

class DealCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization_id = request.data.get('organization_id')
        test_data = request.data.get('test', {})
        
        # Get the current user as the created_by value
        
        
        try:

             # Extract status and probability from test_data
            status_value = test_data.get('stage')
            probability_value = test_data.get('probability')
            deal_name = test_data.get('deal_name')


            deal= Deals.objects.create(
                organization_id=organization_id,
                created_by = request.user,
                name = deal_name,
                created_at=int(timezone.now().timestamp()),
                last_stage_modified=int(timezone.now().timestamp()),
                stage = status_value,
                probability = probability_value
            )

            
            deal_data = {
                'organization_id': organization_id,
                'deal_id': str(deal.id),
                'test': test_data
            }
            deal_collection.insert_one(deal_data)

            return Response({'message': 'Deal created successfully', 'deal_id': str(deal.id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



#  ----------------- update a Deal -----------------------------------
        

class UpdateDealDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            # Retrieve data from the request
            data = request.data
            deal_id = data.get('deal_id')
            updated_test_data = data.get('test', {})  


            status_value = updated_test_data.get('stage')
            probability_value = updated_test_data.get('probability')
            deal_name = updated_test_data.get('deal_name')
            
            # Retrieve the customer instance from the PostgreSQL Customer model
            deal_instance = Deals.objects.get(id=deal_id)
            deal_instance.name = deal_name
            deal_instance.stage = status_value
            deal_instance.probability = probability_value
            deal_instance.last_stage_modified = int(timezone.now().timestamp())
            
            # Save the updated customer instance
            deal_instance.save()

            # Update the document in the MongoDB customer_collection
            result = deal_collection.update_one(
                {'deal_id': deal_id},
                {'$set': {'test': updated_test_data}}
            )

            if result.modified_count > 0:
                return Response({'message': 'Deal details updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No changes detected'}, status=status.HTTP_200_OK)

        except Deals.DoesNotExist:
            return Response({'error': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


#    ----------------- deal delete view -------------------------- 
        
class DeleteDealAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        try:
            # Get customer_id from query parameters
            deal_id = request.query_params.get('deal_id')

            # Check if customer_id is provided
            if not deal_id:
                return Response({'error': 'deal_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the deal from MongoDB
            
            result = deal_collection.delete_one({'deal_id': deal_id})

            # Delete the deal from PostgreSQL
            Deals.objects.filter(id=deal_id).delete()

            if result.deleted_count > 0:
                return Response({'message': 'Deal deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        



#  ----------------------------- deals under a organization -------------------------- 


class DealByOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            organization_id = request.query_params.get('organization_id')
            if not organization_id:
                return Response({'error': 'organization_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve customer data from MongoDB
            deal_data = deal_collection.find({'organization_id': organization_id})

            response_data = []
            for deal in deal_data:
                if 'lead_id' in deal:
                    lead_id = deal['lead_id']
                else:
                    lead_id = None 

                response_data.append({
                    'lead_id': lead_id,
                    'organization_id': deal['organization_id'],
                    'deal_id':deal['deal_id'],

                    'test': deal['test'],
                    
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
          


#    ---------------------   get a deal by deal_id  -----------------------------  
        

class DealDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get deal_id from query parameters
            deal_id = request.query_params.get('deal_id')

            # Check if deal_id is provided
            if not deal_id:
                return Response({'error': 'deal_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve deal details from the database
            deal_instance = Deals.objects.get(id=deal_id)


            created_by_instance = deal_instance.created_by

            deal_data = deal_collection.find_one({'deal_id':deal_id})

            if deal_data:
                deal_data['_id'] = str(deal_data['_id'])


                organization_id = deal_data.get('organization_id')
                organization_instance = Organization.objects.get(id=organization_id )
                organization_name= organization_instance.organization_name

                response_data ={
                    '_id':deal_data['_id'],
                    'organization_id':organization_id,
                    'organization_name':organization_name,
                    'test':deal_data['test'],
                    'created_by_name': created_by_instance.get_full_name() if created_by_instance else None,
                    'created_at':deal_instance.created_at,
                    'last_stage_modified':deal_instance.last_stage_modified,
                }

                if'lead_id' in deal_data:
                    response_data['lead_id'] = deal_data['lead_id']

                else:
                    response_data['lead_id'] = None

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Deal not found'}, status=status.HTTP_404_NOT_FOUND)
            


        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

