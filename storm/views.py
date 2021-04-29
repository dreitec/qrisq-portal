import datetime
import json

from rest_framework.views import APIView
from rest_framework.response import Response

from core.db_connection import query_executor
from .models import StormData
from .serializers import StormDataSerializer
from .storm_file_handler import compressed_geojson_parser, wind_js_parser


class StormDataView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_address = user.profile.address
        storm_data = StormData.objects.filter(qid=user.id)[:1]

        if storm_data.__len__():
            storm_data = storm_data[0]
        else:
            storm_data = None
        storm_data = StormDataSerializer(storm_data).data

        line_data = compressed_geojson_parser('2020-al28-17/line-2020-al28-17-202010282100.json')
        points_data = compressed_geojson_parser('2020-al28-17/points-2020-al28-17-202010282100.json')
        polygon_data = compressed_geojson_parser('2020-al28-17/polygon-2020-al28-17-202010282100.json')

        storm_info = points_data.get('features')[0].get('properties')
        adv_datestring = storm_info.get('ADVDATE')
        advdate = datetime.datetime.strptime(adv_datestring, '%I%M %p CDT %a %b %d %Y')
        next_adv = datetime.timedelta(hours=7, minutes=30)
        next_advdate = advdate + next_adv

        response = {
            'client_id': user.id,
            'storm_name': storm_info.get('STORMNAME'),
            'latitude': user_address.get('lat'),
            'longitude': user_address.get('lng'),
            'address': user_address.get('displayText'),
            'advisory_date': advdate.strftime('%I:%M %p CDT %a %b %d %Y'),
            'next_advisory_date': next_advdate.strftime('%I:%M %p CDT %a %b %d %Y'),
            'line_data': json.dumps(line_data),
            'points_data': json.dumps(points_data),
            'polygon_data': json.dumps(polygon_data),
            **storm_data
        }
        return Response(response)


class WindDataView(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {
            'js_data': wind_js_parser('2020-al28-17/wind-2020-al28-17-202010282100.js'),
            'json_data': json.dumps(compressed_geojson_parser('2020-al28-17/wind-2020-al28-17-202010282100.json'))
        }
        return Response(response_data)
