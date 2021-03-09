import os
# import json
# import logging
from shapely import wkt
from shapely import geometry

from botocore.exceptions import ClientError

from .boto_client import download_file

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


def service_area_finder(latitude, longitude):
    surge_file = 'qrisq-service-area-surge-20210114.wkt'
    wind_file = 'qrisq-service-area-wind-20210114.wkt'

    try:
        if not os.path.exists(wind_file):
            download_file(wind_file)

        if not os.path.exists(surge_file):
            download_file(surge_file)

    except ClientError as e:
        return {
            "status": 500,
            "error": f"WKT files not downloaded; ClientError: {e.response['Error']['Message']}"
        }
    
    try: 
        with open(wind_file, 'r') as wind_reader:
            wind_wkt = wind_reader.read()
        
        with open(surge_file, 'r') as surge_reader:
            surge_wkt = surge_reader.read()

    except FileNotFoundError as err:
        return {
            "status": 500,
            "error": 'WKT files not found'
        }

    # logger.info('Filter Surge WKT: ' + filter_surge_wkt)
    # logger.info('Filter Wind WKT: ' + filter_wind_wkt)
    
    return_data = {
        "status": 200,
        "available": False,
        "services": []
    }

    shape_surge = wkt.loads(surge_wkt)
    shape_wind = wkt.loads(wind_wkt)
    point = geometry.Point(longitude, latitude)

    if shape_surge.contains(point):
        # logger.info('Surge and Wind Service area contains point...')
        return_data['available'] = True
        return_data['services'].append('surge')
    
    if shape_wind.contains(point):
        # logger.info('Surge Service area contains point...')
        return_data['available'] = True
        return_data['services'].append('wind')
   
    return return_data
