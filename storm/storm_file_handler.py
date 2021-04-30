import gzip
import json
import logging
import os
from os.path import basename
from pprint import pprint
import re
from zipfile import ZipFile

from django.conf import settings

from core.boto_client import read_file, list_folder_files, download_file

logger = logging.getLogger(__name__)


def get_latest_files():
    if not os.path.isdir('storm_files'):
        os.makedirs('storm_files')

    # find latest storm data folder
    most_recent_file = settings.AWS_STORM_MOST_RECENT_FILE
    content = read_file(filename=most_recent_file)    # b's3://bucket/latest-folder/'
    latest_folder = content.decode('utf-8').split('/')[-2]

    result = list_folder_files(prefix=latest_folder)
    file_list = result.get('Contents', [])
    files = [fl.get('Key').split("/")[-1] for fl in file_list if fl.get('Key').replace(latest_folder, '') != '/']  # conditional statement to remove folder name from the list

    for filename in files:        
        if not os.path.exists(f"storm_files/{filename}"):
            download_file(
                bucket=settings.AWS_STORM_BUCKET,
                source_filename=f"{latest_folder}/{filename}",
                dest_filename=f"storm_files/{filename}"
            )


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


def surge_zip_creator():
    files = os.listdir('storm_files')
    surge_files = [fil for fil in files if fil.startswith('surge')]

    if not os.path.isdir('zip'):
        os.makedirs('zip')
    zipname = f"zip/{surge_files[0].split('.')[0]}.zip"
    
    with ZipFile(zipname, 'w') as zipobj:
        for filename in surge_files:
            filepath = os.path.join('storm_files', filename)
            zipobj.write(filepath, basename(filepath))
    return zipname