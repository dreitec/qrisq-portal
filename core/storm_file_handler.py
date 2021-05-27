import glob
import gzip
import json
import logging
import os
from os.path import basename
from pprint import pprint
import re
from zipfile import ZipFile
import concurrent.futures as c_futures
import time

from django.conf import settings

from core.boto_client import read_file, list_folder_files, download_file

logger = logging.getLogger(__name__)


def get_latest_files():

    def download(filename):
        start = time.time()
        download_file(
            bucket=settings.AWS_STORM_BUCKET,
            source_filename=f"{latest_folder}/{filename}",
            dest_filename=f"storm_files/{filename}"
        )
        logger.info(f"Downloaded '{filename}' file   --- Download time: {time.time() - start}")

    logger.info("Checking for 'storm_files' folder existence")
    if not os.path.isdir('storm_files'):
        logger.info("Creating 'storm_files'")
        os.makedirs('storm_files')

    # find latest storm data folder
    most_recent_file = settings.AWS_STORM_MOST_RECENT_FILE
    content = read_file(filename=most_recent_file)    # b's3://bucket/latest-folder/'
    latest_folder = content.decode('utf-8').split('/')[-2]
    logger.info(f"Latest Storm data folder: '{latest_folder}'")

    # list the storm files
    result = list_folder_files(prefix=latest_folder)
    file_list = result.get('Contents', [])
    s3_files = {fl.get('Key').split('/')[-1] for fl in file_list if fl.get('Key').replace(latest_folder, '') != '/'}  # conditional statement to remove folder name from the list
    logger.info(f"Latest Storm data files in bucket: '{s3_files}'")

    logger.info("Downloading the missing files")
    existing_files = set(os.listdir('storm_files'))
    download_files = s3_files - existing_files

    # delete outdated files
    [os.remove(f"storm_files/{_file}") for _file in (existing_files - s3_files)]

    # download missing files
    start = time.time()
    with c_futures.ThreadPoolExecutor(max_workers=32) as executor:
        executor.map(download, download_files)  


def compressed_geojson_parser(geojson_compressed_filename):
    logger.debug(f"Parsing geojson compressed file '{geojson_compressed_filename}'")
    try:
        geojson_compressed_file = gzip.open(geojson_compressed_filename,'rb')
        geojson_compressed_data = geojson_compressed_file.read()
        logger.debug(f"'{geojson_compressed_filename}' parsed successfully")
        return json.loads(geojson_compressed_data.decode())
    except FileNotFoundError as err:
        logger.error(f"Geojson file '{geojson_compressed_filename}' not found!!")
        return ""
    except Exception as err:
        logger.warn(f"Geojson file '{geojson_compressed_filename}' parse FAILED: {str(err)}")
        return ""


def wind_js_parser(filename):
    logger.debug(f"Parsing wind JS file '{filename}'")
    try:
        with open(filename, 'r') as f:
            js_string = f.read()
            winddata = js_string.partition('=')[-1]  # get only the wind data value
            json_string = re.sub(' +', '', winddata)
            logger.debug(f"Wind JS file '{filename}' parsed successfully")
            return json.dumps(json.loads(json_string))
    except FileNotFoundError as err:
        logger.warn(f"Wind JS file '{filename}' not found")
        return ""
    except Exception as err:
        logger.warn(f"Wind js file '{filename}' parse FAILED: {str(err)}")
        return ""


def surge_zip_creator():
    logger.info("Creating Surge files zip")
    files = os.listdir('storm_files')
    surge_files = [fil for fil in files if fil.startswith('surge')]

    try:
        if not os.path.isdir('zip'):
            logger.debug("Creating zip folder to store zip file")
            os.makedirs('zip')

        zipname = f"zip/{surge_files[0].split('.')[0]}.zip"
        logger.info(f"Zip file name: {zipname}")

        if not os.path.exists(zipname):
            # remove all other old zip files
            [os.remove(f) for f in glob.glob('zip/*', recursive=True)]
            with ZipFile(zipname, 'w') as zipobj:
                for filename in surge_files:
                    filepath = os.path.join('storm_files', filename)
                    zipobj.write(filepath, basename(filepath))
        logger.debug(f"{zipname} file created successfully")
        return zipname 
    
    except Exception as err:
        logger.warn(f"Error creating surge files zip: {str(err)}")
        return ""