import os
import logging

from django.conf import settings

from shapely import wkt
from shapely import geometry
from shapely.errors import WKTReadingError

from botocore.exceptions import ClientError, ParamValidationError

from .boto_client import download_file

logger = logging.getLogger(__name__)


def service_area_finder(latitude, longitude):
    surge_file = './qrisq-service-area-surge-20210114.wkt'
    wind_file = './qrisq-service-area-wind-20210114.wkt'

    try:
        logger.info("Checking for wind WKT file existence")
        if not os.path.exists(wind_file):
            download_file(bucket=settings.AWS_WKT_BUCKET, source_filename=wind_file, dest_filename=wind_file)

        with open(wind_file, 'r') as wind_reader:
            wind_wkt = wind_reader.read()
            shape_wind = wkt.loads(wind_wkt)
            logger.info(f"Wind WKT file data Parsed")
    except ClientError as e:
        return {
            "status": 500,
            "error": f"Wind WKT file not downloaded; ClientError: {e.response['Error']['Message']}"
        }
    except ParamValidationError as err:
        return {
            "status": 500,
            "error": f"Wind WKT file not downloaded; ParamValidationError: Invalid bucket name"
        }
    except FileNotFoundError as err:
        logger.warn(f"{wind_file} not found")
        return {
            "status": 500,
            "error": 'Wind WKT file not found'
        }
    except WKTReadingError as err:
        logger.warn(f"{wind_file} read error: Deleting the file")
        os.remove(wind_file)
        logger.info(f"{wind_file} removed.")
        return {
            "status": 500,
            "error": "Wind WKT file is corrupted. Please try again in a while."
        }
    
    try:
        logger.info("Checking for surge WKT file existence")
        if not os.path.exists(surge_file):
            download_file(settings.AWS_WKT_BUCKET, source_filename=surge_file, dest_filename=surge_file)
        
        with open(surge_file, 'r') as surge_reader:
            surge_wkt = surge_reader.read()
            shape_surge = wkt.loads(surge_wkt)
            logger.info(f"Surge WKT file data Parsed")

    except ClientError as e:
        return {
            "status": 500,
            "error": f"Surge WKT file not downloaded; ClientError: {e.response['Error']['Message']}"
        }
    except ParamValidationError as err:
        return {
            "status": 500,
            "error": f"Wind WKT file not downloaded; ParamValidationError: Invalid bucket name"
        }
    except FileNotFoundError as err:
        logger.warn(f"{surge_file} not found")
        return {
            "status": 500,
            "error": 'Surge WKT file not found'
        }
    except WKTReadingError as err:
        logger.warn(f"{surge_file} read error: Deleting the file")
        os.remove(surge_file)
        logger.info(f"{surge_file} removed.")
        return {
            "status": 500,
            "error": "Surge WKT file is corrupted. Please try again in a while."
        }
    
    return_data = {
        "status": 200,
        "available": False,
        "services": []
    }

    point = geometry.Point(longitude, latitude)
    logger.info(f"Requested Point data: {point}")
    if shape_surge.contains(point):
        logger.info(f"Point {point} found in Surge service area")
        return_data['available'] = True
        return_data['services'].append('surge')
    
    if shape_wind.contains(point):
        logger.info(f"Point {point} found in Wind service area")
        return_data['available'] = True
        return_data['services'].append('wind')

    logger.info(f"Response data for latitude {latitude} and longitude {longitude}: {return_data}")
    return return_data
