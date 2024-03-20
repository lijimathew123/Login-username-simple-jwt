from rest_framework import serializers
from .models import *
from .models import DefaultCompanyFields
from django.conf import settings
from account_app.models import Organization




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'





class DefaultCompanyFieldsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = DefaultCompanyFields
        fields = '__all__'





class DefaultCompanyFieldsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    field_type = serializers.SerializerMethodField(read_only=True)
   


    class Meta:
        model = DefaultCompanyFields
        fields = '__all__'

    def get_category(self, obj):
        if obj.catogory:  
            return {'id': obj.catogory.id, 'name': obj.catogory.name, 'order': obj.catogory.order}
        else:
            return None
        
    # def get_field_type(self, obj):
    #     if obj.field_type:  
    #         return {'id': obj.field_type.id, 'name': obj.field_type.name}
    #     else:
    #         return None
        
    def get_field_type(self, obj):
        if obj.field_type:
            field_type_data = {
                'id': obj.field_type.id,
                'name': obj.field_type.name
            }
            if obj.field_type.icon:
                field_type_data['icon_url'] = obj.field_type.icon.url
            return field_type_data
        else:
            return None
        

    

    



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('organization_name', )


