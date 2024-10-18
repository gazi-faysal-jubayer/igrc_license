from rest_framework import serializers
from .models import Agency

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['name', 'organization_type', 'email', 'address', 'phone_number', 'profile_picture']
        read_only_fields = ['created_by']  # Make created_by read-only
