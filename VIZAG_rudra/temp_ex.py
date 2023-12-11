import cv2
import numpy as np
from PIL import Image

def save_as_16bit_tiff(gray_image, output_path):
    # Convert 8-bit grayscale to 16-bit grayscale
    gray_16bit = np.uint16(gray_image * (65535 / 255))
    # Save as 16-bit TIFF
    Image.fromarray(gray_16bit).save(output_path, format='TIFF')

def mouse_move(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        pixel_value = param[y, x]
        temperature = map_temperature(pixel_value)
        print(f"Temperature at ({x}, {y}): {temperature:.2f}°C")

def map_temperature(pixel_value):
    # Assuming a simple linear mapping for demonstration purposes
    min_temp = 500  # Min temperature in degrees Celsius
    max_temp = 1500  # Max temperature in degrees Celsius
    return ((pixel_value / 65535) * 1500)

# Path to the input image
input_image_path = "ladle_hot.webp"
# Path to the output TIFF image
output_tiff_path = 'ladle_hot_16bit.tiff'

# Read the image in grayscale
image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save the grayscale image as a 16-bit TIFF
save_as_16bit_tiff(gray_image, output_tiff_path)

# Read the 16-bit TIFF image
gray_16bit_image_pil = Image.open(output_tiff_path)
gray_16bit_image = np.array(gray_16bit_image_pil, dtype=np.uint16)

# Convert the 16-bit image to 8-bit for display
gray_8bit_image = np.uint8(gray_16bit_image / 256)

# Apply a colormap for visualization
colored_image = cv2.applyColorMap(gray_8bit_image, cv2.COLORMAP_HOT)

# Create a window and set a mouse callback function
cv2.namedWindow('Temperature Visualization')
cv2.setMouseCallback('Temperature Visualization', mouse_move, gray_16bit_image)

# Display the image
while True:
    cv2.imshow('Temperature Visualization', colored_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the window
cv2.destroyAllWindows()
