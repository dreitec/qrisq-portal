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
    try:
        if not os.path.exists("surge.wkt"):
            download_file('qrisq-service-area-surge-20210114.wkt')

        if not os.path.exists("wind.wkt"):
            download_file('qrisq-service-area-wind-20210114.wkt')
    except ClientError as e:
        return_body = 'WKT files not downloaded; ClientError: ' + e.response['Error']['Message']
        return_status_code = 500
    else:
        # logger.info('Service Area WKT files downloaded.')
        print("")

    with open("wind.wkt", 'r') as wind_reader:                
        filter_wind_wkt = wind_reader.read().decode()
    
    with open("surge.wkt", 'r') as surge_reader:
        filter_surge_wkt = surge_reader.read().decode()     
        
    # logger.info('Filter Surge WKT: ' + filter_surge_wkt)
    # logger.info('Filter Wind WKT: ' + filter_wind_wkt)
    
    shape_surge_filter = wkt.loads(filter_surge_wkt)
    shape_wind_filter = wkt.loads(filter_wind_wkt)

    point = geometry.Point(longitude, latitude)

    #'surge_and_wind'; 'surge_only'; 'wind_only'; 'no_service'
    if shape_surge_filter.contains(point) and shape_wind_filter.contains(point):
        # logger.info('Surge and Wind Service area contains point...')
        return_status_code = 200
        return_body = 'surge_and_wind'
    elif shape_surge_filter.contains(point) and not shape_wind_filter.contains(point):
        # logger.info('Surge Service area contains point...')
        return_status_code = 200
        return_body = 'surge_only'
    elif not shape_surge_filter.contains(point) and  shape_wind_filter.contains(point):
        # logger.info('Wind Service area contains point...')
        return_status_code = 200
        return_body = 'wind_only'
    else:
        # logger.info('Service area does not contain point...')
        return_status_code = 200
        return_body = 'no_service'    
    
    return {
        'statusCode': return_status_code,
        #'body': json.dumps(return_body)
        'body': return_body
    }
