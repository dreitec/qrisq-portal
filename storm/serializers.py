import datetime

from rest_framework import serializers
from .models import StormData


class StormDataSerializer(serializers.ModelSerializer):
    surgerisk = serializers.CharField(source='riskthreat')
    advisory_wind_date = serializers.CharField(source='maxwind_datetime_local_string')
    advisory_flood_date = serializers.CharField(source='maxflood_datetime_local_string')

    class Meta:
        model = StormData
        fields = ('windrisk', 'surgerisk', 'maxflood', 'landfall_location', 'landfall_datetime',
                  'storm_distance', 'maxflood_datetime', 'maxwind_datetime', 'advisory_wind_date',
                  'advisory_flood_date')

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['next_advisory_wind_date'] = None
        data['next_advisory_flood_date'] = None

        if data['advisory_wind_date']:
            wind_date = " ".join(data['advisory_wind_date'][1:].split(" on "))
            wind_advdate = datetime.datetime.strptime(wind_date, '%I%p CDT %a %b %d %Y')
            next_wind_advdate = datetime.timedelta(hours=7, minutes=30)
            next_wind_advdate = wind_advdate + next_wind_advdate
            data['next_advisory_wind_date'] = f"~{next_wind_advdate.strftime('%I%p CDT %a %b %d %Y')}"

        if data['advisory_wind_date']:
            flood_date = " ".join(data['advisory_flood_date'][1:].split(" on "))
            flood_advdate = datetime.datetime.strptime(flood_date, '%I%p CDT %a %b %d %Y')
            next_flood_advdate = datetime.timedelta(hours=7, minutes=30)
            next_flood_advdate = flood_advdate + next_flood_advdate
            data['next_advisory_flood_date'] = f"~{next_flood_advdate.strftime('%I%p CDT %a %b %d %Y')}"
        return data
