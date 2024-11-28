import os
import time
from samsungtvws import SamsungTVWS
import argparse

args = parser.parse_args()



IMAGE_DIRECTORY = "/media/frame"


parser = argparse.ArgumentParser(description='Upload images to Samsung TV.')
parser.add_argument('--tvip', help='IP address of the Samsung the Frame')

tvip = args.tvip

def upload_and_display_image(image_path):
    try:
        # Connect to the TV
        tv = SamsungTVWS(host=tvip)
        art = tv.art()

        # Read the image
        with open(image_path, "rb") as f:
            image_data = f.read()

        print(f"Now Uploading {image_path}...")
        # Upload the image
        response = art.upload(
            image_data,
            file_type="JPEG",
            matte="modern_apricot"  # Adjust matte and color as needed
        )
        print(f"Uploaded {image_path}: {response}")

        # Assuming the response is the image ID directly
        image_id = response  # Directly use the string if it's the ID
        print("Activating Art Mode and displaying the uploaded image...")
        art.select_image(image_id)  # Pass the image ID to set it in Art Mode
        tv.send_key("KEY_POWERON")  # Ensure the TV is ON
        time.sleep(2)  # Give time for the TV to process

        print("Art Mode activated with the uploaded image.")
        print(f"{time.ctime()}")
    except Exception as e:
        print(f"Error: {e}")

def upload_images_in_directory(directory):
    # Connect to the TV
    tv = SamsungTVWS(host=tvip)
    art = tv.art()

    # Get the list of existing images on the TV
    existing_images = art.list()

    # List all .jpg files in the directory
    files = [filename for filename in os.listdir(directory) if filename.lower().endswith(".jpg")]

    # Filter out images that are already on the TV
    files_to_upload = [f for f in files if f not in existing_images]

    # Upload all images that are not already on the TV
    for image in files_to_upload:
        full_path = os.path.join(directory, image)
        upload_and_display_image(full_path)
        # Sleep 2 seconds to let the Frame TV process the image
        time.sleep(2)
def display_random_image():
    try:
        # Connect to the TV
        tv = SamsungTVWS(host=tvip)
        art = tv.art()

        # Get the list of existing images on the TV
        existing_images = art.list()

        if not existing_images:
            print("No images available on the TV.")
            return

        # Randomly select an image
        selected_image = random.choice(existing_images)
        print(f"Randomly selected image: {selected_image}")

        # Display the selected image
        art.select_image(selected_image)  # Pass the image ID to set it in Art Mode
        tv.send_key("KEY_POWERON")  # Ensure the TV is ON
        time.sleep(2)  # Give time for the TV to process

        print("Art Mode activated with the randomly selected image.")
        print(f"{time.ctime()}")
    except Exception as e:
        print(f"Error: {e}")

# Call the function to upload and display images
upload_images_in_directory(IMAGE_DIRECTORY)

display_random_image()