from PIL import Image
import os

# Folder containing the images
input_folder = "input_images"
output_folder = "output_images"

# Target size
target_width = 800
target_height = 450

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")

        with Image.open(input_path) as img:
            # Calculate new size preserving aspect ratio
            img_ratio = img.width / img.height
            target_ratio = target_width / target_height

            if img_ratio > target_ratio:
                # Image is wider → width fits, height padded
                new_width = target_width
                new_height = round(target_width / img_ratio)
            else:
                # Image is taller → height fits, width padded
                new_height = target_height
                new_width = round(target_height * img_ratio)

            # Resize image
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)

            # Create black background
            new_img = Image.new("RGB", (target_width, target_height), (0, 0, 0))
            
            # Paste resized image in center
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
            new_img.paste(img_resized, (paste_x, paste_y))

            # Save as JPG
            new_img.save(output_path, "JPEG", quality=95)

print("Conversion completed!")

