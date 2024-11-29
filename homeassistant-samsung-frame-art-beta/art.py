import sys
import random
import json
import os
import asyncio
import logging
import argparse
from PIL import Image


sys.path.append('../')

from samsungtvws.async_art import SamsungTVAsyncArt
from samsungtvws import exceptions



logging.basicConfig(level=logging.INFO) #or logging.DEBUG to see messages

def parseargs():
    # Add command line argument parsing
    parser = argparse.ArgumentParser(description='Example async art Samsung Frame TV.')
    parser.add_argument('--ip', action="store", type=str, default=None, help='ip address of TV (default: %(default)s))')
    parser.add_argument('--filter', action="store", type=str, default=None, help='photo filter to apply (default: %(default)s))')
    parser.add_argument('--matte', action="store", type=str, default=None, help='matte to apply (default: %(default)s))')
    return parser.parse_args()
    


# Set the path to the folder containing the images
folder_path = '/media/frame'
# folder_path = './frame'

async def main():
    args = parseargs()
    tv = SamsungTVAsyncArt(host=args.ip, port=8002)
    await tv.start_listening()
    

    supported = await tv.supported()
    if supported:
        logging.info('This TV is supported')

    else:
        logging.info('This TV is not supported')
   
    if supported:
        try:
            #is tv on (calls tv rest api)
            tv_on = await tv.on()
            logging.info('tv is on: {}'.format(tv_on))
            
            #is art mode on
            #art_mode = await tv.get_artmode()                  #calls websocket command to determine status
            art_mode = tv.art_mode                              #passive, listens for websocket messgages to determine art mode status
            logging.info('art mode is on: {}'.format(art_mode))

            #get current artwork
            info = await tv.get_current()
            # logging.info('current artwork: {}'.format(info))
            current_content_id = info['content_id']

            photos = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg'))]
            if not photos:
                logging.info('No PNG or JPG photos found in the folder')
                return
            else:
                filename = random.choice(photos)
                filename = os.path.join(folder_path, filename)
                new_filename = os.path.join(folder_path, os.path.basename(filename).lower())
                os.rename(filename, new_filename)
                filename = new_filename
                logging.info('Selected and renamed photo: {}'.format(filename))


                image = Image.open(filename)
                new_image = image.resize((3840, 2160))
                new_image.save(filename)



                content_id = None
                if filename:
                    with open(filename, "rb") as f:
                        file_data = f.read()
                    file_type = os.path.splitext(filename)[1][1:] 
                    content_id = await tv.upload(file_data, file_type=file_type, matte=args.matte) 
                    logging.info('uploaded {} to tv as {}'.format(filename, content_id))
                    await tv.set_photo_filter(content_id, args.filter)

                    await tv.select_image(content_id, show=True)
                    logging.info('set artwork to {}'.format(content_id))

               
                    #delete the file that was showing before
                    
                    await tv.delete_list([current_content_id])
                    logging.info('deleted from tv: {}'.format([current_content_id]))  

                    await tv.get_matte_list(include_colour=True)
                    logging.info('matte list: {}'.format(await tv.get_matte_list()))
                      





            await asyncio.sleep(15)

        except exceptions.ResponseError as e:
            logging.warning('ERROR: {}'.format(e))
        except AssertionError as e:
            logging.warning('no data received: {}'.format(e))

        
    await tv.close()


asyncio.run(main())

# if float(api_version) < 3.0:
#     logging.info('old tv')
# else:
#     logging.info('new tv')

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
