from rest_framework import serializers
from .models import DefaultCustomerFields

class DefaultCustomerFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultCustomerFields
        fields = '__all__'
