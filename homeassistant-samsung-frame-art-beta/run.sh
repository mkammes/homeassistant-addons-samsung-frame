#!/usr/bin/with-contenv bashio

TVIP=$(bashio::config 'tv')
FILTER=$(bashio::config 'filter')
MATTE=$(bashio::config 'matte')

mkdir -p /media/frame
echo "Using ${TVIP} as the IP of the Samsung Frame"
python3 art.py --ip ${TVIP} --filter "${FILTER}" --matte "${MATTE}"
echo "done, closing now!"
kill -s SIGHUP 1

