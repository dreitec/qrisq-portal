from rest_framework import serializers
from .models import WktFile


class ServiceAreaSerializer(serializers.Serializer):
    latitude = serializers.FloatField(max_value=90.0000000, min_value=-90.0000000)
    longitude = serializers.FloatField(max_value=180.0000000, min_value=-180.0000000)


class WktFileSerializer(serializers.ModelSerializer):
    class Meta:
        models = WktFile
        fields = "__all__"
