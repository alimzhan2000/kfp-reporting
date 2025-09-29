from rest_framework import serializers
from .models import DataUpload


class DataUploadSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = DataUpload
        fields = (
            'id', 'file_name', 'file_size', 'status', 'records_processed', 
            'records_created', 'records_updated', 'error_message', 
            'uploaded_by_name', 'created_at', 'completed_at'
        )
        read_only_fields = ('id', 'uploaded_by_name', 'created_at', 'completed_at')

