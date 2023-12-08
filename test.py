import cv2
import numpy as np

# Load an infrared image (replace 'your_image_path' with the actual path)
image = cv2.imread("gray16_image.png", cv2.IMREAD_GRAYSCALE)

# Apply color mapping for visualization
colored_image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

# Display the original and processed images
cv2.imshow('Original Image', image)
cv2.imshow('Colored Image', colored_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
