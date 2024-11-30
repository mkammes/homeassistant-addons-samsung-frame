import os
import sys
import time
import logging
from samsung_frame import FrameTV

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Get config from environment
    tv_ip = os.environ.get('TV_IP', '192.168.1.107')
    image_folder = os.environ.get('IMAGE_FOLDER', '/media/frame')
    specific_image = os.environ.get('IMAGE_PATH', '')

    # Initialize Frame TV
    try:
        tv = FrameTV(tv_ip)
        logger.info(f"Connected to Frame TV at {tv_ip}")
    except Exception as e:
        logger.error(f"Failed to connect to Frame TV: {e}")
        sys.exit(1)

    # If specific image is provided, use that
    if specific_image:
        if os.path.exists(specific_image):
            logger.info(f"Displaying specific image: {specific_image}")
            tv.display_image(specific_image)
            return
        else:
            logger.error(f"Specified image does not exist: {specific_image}")
            sys.exit(1)

    # Otherwise, monitor folder for changes
    while True:
        try:
            # Check for new images
            images = [f for f in os.listdir(image_folder)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if images:
                image_path = os.path.join(image_folder, images[0])
                logger.info(f"Sending image {image_path} to Frame TV")
                tv.display_image(image_path)

            time.sleep(30)  # Check every 30 seconds

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            time.sleep(60)  # Wait before retrying


if __name__ == "__main__":
    main()
