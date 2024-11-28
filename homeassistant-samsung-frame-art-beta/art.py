import os
import time
from samsungtvws import SamsungTVWS

IMAGE_DIRECTORY = "/media/frame"
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
    # List all .jpg files and sort them alphabetically
    files = sorted(
        [filename for filename in os.listdir(
            directory) if filename.lower().endswith(".jpg")]
    )

    # Loop through sorted filenames
    for filename in files:
        full_path = os.path.join(directory, filename)
        upload_and_display_image(full_path)
        # Sleep 2 seconds to let the Frame TV process the image
        time.sleep(2)


# Call the function to upload and display images
upload_images_in_directory(IMAGE_DIRECTORY)