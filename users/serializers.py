from rest_framework import serializers
from .models import *

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['name', 'organization_type', 'email', 'address', 'phone_number', 'profile_picture']
        read_only_fields = ['created_by']  # Make created_by read-only

class LicenseSerializer(serializers.ModelSerializer):
    agency = serializers.SlugRelatedField(slug_field='name', queryset=Agency.objects.all())
    license_id = serializers.IntegerField(source='id', read_only=True)  # Map 'id' to 'license_id'

    class Meta:
        model = License
        fields = ['license_id', 'agency', 'details', 'number_of_licenses', 'per_license_price', 'hosting_by', 'hosting_cost']