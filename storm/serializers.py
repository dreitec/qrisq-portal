from rest_framework import serializers
from .models import StormData


class StormDataSerializer(serializers.ModelSerializer):
    surgerisk = serializers.CharField(source='riskthreat')

    class Meta:
        model = StormData
        fields = ('windrisk', 'surgerisk', 'maxflood', 'landfall_location', 'landfall_datetime', 'storm_distance')
