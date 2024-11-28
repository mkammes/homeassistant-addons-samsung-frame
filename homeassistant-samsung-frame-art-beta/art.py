#!/usr/bin/env python3
# NOTE old api is 2021 and earlier Frame TV's, new api is 2022+ Frame TV's

import os
import asyncio
import logging
import argparse

from samsungtvws.async_art import SamsungTVAsyncArt
from samsungtvws import exceptions

logging.basicConfig(level=logging.INFO) #or logging.DEBUG to see messages

def parseargs():
    # Add command line argument parsing
    parser = argparse.ArgumentParser(description='Example async art Samsung Frame TV.')
    parser.add_argument('ip', action="store", type=str, default=None, help='ip address of TV (default: %(default)s))')
    return parser.parse_args()
    
async def image_callback(event, response):
    logging.info('CALLBACK: image callback: {}, {}'.format(event, response))

async def main():
    args = parseargs()
    tv = SamsungTVAsyncArt(host=args.ip, port=8002)
    await tv.start_listening()
    
    #is art mode supported
    supported = await tv.supported()
    logging.info('art mode is supported: {}'.format(supported))
    
    if supported:
        try:
            #is tv on (calls tv rest api)
            tv_on = await tv.on()
            logging.info('tv is on: {}'.format(tv_on))
            
            #is art mode on
            #art_mode = await tv.get_artmode()                  #calls websocket command to determine status
            art_mode = tv.art_mode                              #passive, listens for websocket messgages to determine art mode status
            logging.info('art mode is on: {}'.format(art_mode))
            
            #check both with one call (calls tv rest api)
            logging.info('tv is on and in art mode: {}'.format(await tv.is_artmode()))
            
            #get api version 4.3.4.0 is new api, 2.03 is old api
            api_version = await tv.get_api_version()
            logging.info('api version: {}'.format(api_version))
            

            
            # Request list of all art
            try:
                info = await tv.available()
                #info = await tv.available('MY-C0002')              #gets list of uploaded art, MY-C0004 is favourites
            except AssertionError:
                info='None'
            logging.info('artwork available on tv: {}'.format(info))

            
            #or get slideshow status, old api fails silently on new TV's, but throws AssertionError on older ones
            try:
                info = await tv.get_auto_rotation_status()
            except AssertionError:
                info = await tv.get_slideshow_status()
            logging.info('current slideshow status: {}'.format(info))
            
            
            #upload file
            '''
            filename = "framed_IMG_0181.png"
            content_id = None
            if filename:
                with open(filename, "rb") as f:
                    file_data = f.read()
                file_type = os.path.splitext(filename)[1][1:] 
                content_id = await tv.upload(file_data, file_type=file_type)
                content_id = os.path.splitext(content_id)[0]    #remove file extension if any (eg .jpg)
                logging.info('uploaded {} to tv as {}'.format(filename, content_id))
                
            #delete art on tv
            if content_id:
                await tv.delete_list([content_id])
                logging.info('deleted from tv: {}'.format([content_id]))
            '''
            
            
            
            await asyncio.sleep(15)
        except exceptions.ResponseError as e:
            logging.warning('ERROR: {}'.format(e))
        except AssertionError as e:
            logging.warning('no data received: {}'.format(e))

    await tv.close()


asyncio.run(main())