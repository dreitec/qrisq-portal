from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.service_area import service_area_finder as finder


@api_view(['POST'])
def check_service_area(request):
    if finder(1, 2):
        return Response("file exists")
    return Response("file doesn't exist")
