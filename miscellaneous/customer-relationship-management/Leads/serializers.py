from rest_framework import serializers
from company.models import *

from .models import DefaultLeadFields

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' 