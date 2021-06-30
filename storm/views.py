import datetime
import json
import os
import concurrent.futures as c_futures

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.response import Response
from rest_framework.views import APIView

from core.db_connection import query_executor
from core.storm_file_handler import get_latest_files, compressed_geojson_parser, wind_js_parser, surge_zip_creator
from .models import StormData
from .serializers import StormDataSerializer


class StormDataView(APIView):
    def get(self, request, *args, **kwargs):
        # check and download latest storm data files
        get_latest_files()

        storm = None
        user = request.user

        if user:
            user_profile = getattr(user, 'profile', None)
            user_address = getattr(user_profile, 'address', {})
            storm_data = StormData.objects.filter(qid=user.id)[:1]

            if storm_data.__len__():
                storm = storm_data[0]

        storm_data = StormDataSerializer(storm).data

        files = os.listdir('storm_files')
        storm_files = sorted([f"storm_files/{f}" for f in files if f.startswith('line') or f.startswith('points') or f.startswith('polygon')])

        with c_futures.ThreadPoolExecutor(max_workers=5) as executor:
            line_data, points_data, polygon_data = executor.map(compressed_geojson_parser, storm_files)

        storm_info = points_data.get('features')[0].get('properties')
        adv_datestring = storm_info.get('ADVDATE')

        # strip timezone
        hr_min, am_pm, timezone, *date_year = adv_datestring.split(" ")
        advdatetime_with_no_timezone = f"{hr_min} {am_pm} {(' '.join(date_year))}"
        advdate = datetime.datetime.strptime(advdatetime_with_no_timezone, '%I%M %p %a %b %d %Y')
        next_adv = datetime.timedelta(hours=7, minutes=30)
        next_advdate = advdate + next_adv

        # add timezone
        advisory_dtstring = advdate.strftime(f"%I:%M %p {timezone} %a %b %d %Y")
        next_advisory_dtstring = next_advdate.strftime(f"%I:%M %p {timezone} %a %b %d %Y")

        response = {
            'has_data': storm is not None,
            'client_id': user.id,
            'storm_name': storm_info.get('STORMNAME'),
            'latitude': user_address.get('lat'),
            'longitude': user_address.get('lng'),
            'address': user_address.get('displayText'),
            'advisory_date': advisory_dtstring,
            'next_advisory_date': next_advisory_dtstring,
            'line_data': json.dumps(line_data),
            'points_data': json.dumps(points_data),
            'polygon_data': json.dumps(polygon_data),
            **storm_data
        }
        return Response(response)


class SurgeDataView(APIView):
    def get(self, request, *args, **kwargs):
        # check and download latest storm data files
        get_latest_files()

        filename = surge_zip_creator()
        return Response({'url': f"{settings.DOMAIN}/api/{filename}"})


class WindDataView(APIView):
    def get(self, request, *args, **kwargs):
        # check and download latest storm data files
        get_latest_files()

        files = os.listdir('storm_files')
        wind_files = sorted(filter(lambda fil: fil.startswith('wind'), files))
        response_data = {
            'js_data': wind_js_parser(f"storm_files/{wind_files[0]}"),
            'json_data': json.dumps(compressed_geojson_parser(f"storm_files/{wind_files[1]}"))
        }
        return Response(response_data)
