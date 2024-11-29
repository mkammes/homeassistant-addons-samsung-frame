import sys
import logging
import os
import random
import json
import argparse


sys.path.append('../')

from samsungtvws import SamsungTVWS


# Add command line argument parsing
parser = argparse.ArgumentParser(description='Upload images to Samsung TV.')
parser.add_argument('--ip', help='IP address of the Samsung the Frame')
args = parser.parse_args()

# Parse the command line arguments
ip = args.ip

# Set the path to the folder containing the images
folder_path = '/media/frame'

# Set the path to the file that will store the list of uploaded filenames
upload_list_path = '/data/uploaded_files.json'

# Load the list of uploaded filenames from the file
if os.path.isfile(upload_list_path):
		with open(upload_list_path, 'r') as f:
				uploaded_files = json.load(f)
else:
		uploaded_files = []



# Increase debug level
logging.basicConfig(level=logging.INFO)

# Normal constructor
tv = SamsungTVWS(ip)


api_version = tv.get_api_version()
logging.info('api version: {}'.format(api_version))
# # Is art mode supported?
# info = tv.art().supported()
# logging.info(info)

# if tv.art().supported():
#     available_art = tv.art().available()
#     logging.info("Available art: %s", available_art)

# # List the art available on the device
# info = tv.art().available()
# logging.info(info)

# # Retrieve information about the currently selected art
# info = tv.art().get_current()
# logging.info(info)

# # Retrieve a thumbnail for a specific piece of art. Returns a JPEG.
# thumbnail = tv.art().get_thumbnail('SAM-F0206')


# # Determine whether the TV is currently in art mode
# info = tv.art().get_artmode()
# logging.info(info)

# # List available photo filters
# info = tv.art().get_photo_filter_list()
# logging.info(info)
