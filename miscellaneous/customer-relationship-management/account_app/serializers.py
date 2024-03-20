from rest_framework import serializers
from .models import (
        PlatformCustomer,
        PlatformCustomerDetails,
        Organization, 
        OrganizationBranch, 
        SocialChannel,
        FieldType
        
)

from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.utils import timezone
from calendar import timegm
from datetime import datetime


from .models import CustomerType

class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = '__all__'



# ---------serializer for handle platform customer------------------------
        
class PlatformCustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    customer_type = CustomerTypeSerializer()

    class Meta:
        model = PlatformCustomer
        fields = '__all__'
        read_only_fields = ['is_email_verified','is_phone_verified']

    # def create(self, validated_data):
        # # Handle creation of nested objects here
        # customer_type_data = validated_data.pop('customer_type', None)
        # if customer_type_data:
        #     customer_type_instance, _ = CustomerType.objects.get_or_create(**customer_type_data)
        #     validated_data['customer_type'] = customer_type_instance

        #  # Set created_at to the current timestamp
        # validated_data['created_at'] = timezone.now().timestamp()
        

        # # Call the super method to create the PlatformCustomer instance
        # instance = super().create(validated_data)

        # return instance
    
   
    


class PlatformCustomerSerializer2(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    customer_type = CustomerTypeSerializer()

    class Meta:
        model = PlatformCustomer
        fields = '__all__'

    

    def create(self, validated_data):
        # Extract the customer_type data from validated_data
        customer_type_data = validated_data.pop('customer_type', None)

        # Create or get the CustomerType instance
        customer_type_instance = None
        if customer_type_data:
            customer_type_instance, _ = CustomerType.objects.get_or_create(**customer_type_data)

        # Set is_email_verified to False initially
        validated_data['is_email_verified'] = False
        validated_data['password'] =  make_password(validated_data['password'])

        # Create the PlatformCustomer instance with the rest of the data
        platform_customer_instance = PlatformCustomer.objects.create(customer_type=customer_type_instance, **validated_data)

        return platform_customer_instance
    

  
    
    
    def update(self, instance, validated_data):
        # Handle updating of nested serializer (customer_type)
        customer_type_data = validated_data.pop('customer_type', None)
        if customer_type_data:
            customer_type_instance, _ = CustomerType.objects.get_or_create(**customer_type_data)
            instance.customer_type = customer_type_instance

        # Update the other fields
        instance.phone = validated_data.get('phone', instance.phone)
        instance.source = validated_data.get('source', instance.source)
        instance.phone = validated_data.get('customer_type', instance.phone)
     
       

        # Save the changes
        instance.save()

        return instance

# ----------serializer for add more details of platform customer--------------------

class PlatfromCustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformCustomerDetails
        fields = '__all__'

       


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationBranch
        fields = '__all__'
        


# ------------------serializers for social channel ----------------------
        
class SocialChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialChannel
        fields = '__all__'


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = '__all__'