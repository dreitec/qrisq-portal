import math
import gzip
import json
import logging
import re

from core.boto_client import download_storm_file, list_storm_folders

logger = logging.getLogger(__name__)


def download_latest_files():
    result = list_storm_folders()
    for o in result.get('CommonPrefixes'):
        print(o.get('Prefix'))


def compressed_geojson_parser(geojson_compressed_filename):
    try:
        geojson_compressed_file = gzip.open(geojson_compressed_filename,'rb')
        geojson_compressed_data = geojson_compressed_file.read()
        return json.loads(geojson_compressed_data.decode())
    except Exception as err:
        pass


def wind_js_parser(filename):
    try:
        with open(filename, 'r') as f:
            js_string = f.read()
            winddata = js_string.partition('=')[-1]  # get only the wind data value
            json_string = re.sub(' +', '', winddata)
            return json.dumps(json.loads(json_string))
    except FileNotFoundError as err:
       pass