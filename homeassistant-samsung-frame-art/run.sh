#!/usr/bin/env bashio
set -e

# Get config values
TV_IP=$(bashio::config 'tv_ip')
IMAGE_FOLDER=$(bashio::config 'image_folder')
IMAGE_PATH=$(bashio::config 'image_path')

# Run the Python script
python3 /run.py

