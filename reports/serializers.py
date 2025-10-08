from rest_framework import serializers
from .models import AgriculturalData, ReportTemplate


class AgriculturalDataSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = AgriculturalData
        fields = (
            'id', 'field_name', 'year', 'planting_area', 'yield_per_hectare',
            'crop', 'variety', 'final_product', 'uploaded_by_name', 
            'created_at', 'updated_at', 'total_yield'
        )
        read_only_fields = ('id', 'uploaded_by_name', 'created_at', 'updated_at', 'total_yield')


class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'


