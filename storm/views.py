from rest_framework.views import APIView
from rest_framework.response import Response

from core.db_connection import query_executor
from .models import StormData
from .serializers import StormDataSerializer


class StormDataView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_address = user.profile.address
        storm_data = StormData.objects.filter(qid=user.id)

        if storm_data.__len__():
            storm_data = storm_data[0]
        else:
            storm_data = storm_data.first()
        storm_data = StormDataSerializer(storm_data).data
        
        response = {
            'client_id': user.id,
            'storm_name': "Hurricane Zeta",
            'latitude': user_address.get('lat'),
            'longitude': user_address.get('lng'),
            'address': user_address.get('displayText'),
            'advisory_date': None,
            'next_advisory_date': None,
            **storm_data
        }
        return Response(response)