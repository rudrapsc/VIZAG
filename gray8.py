from PIL import Image

# Open the image
img = Image.open(r"C:\Users\YASH\Downloads\laddle3.png")

# Convert the image to 8-bit grayscale
img_gray = img.convert('L')

# Simulate 16-bit grayscale
# This step assumes that the original 8-bit grayscale values should be spread over the 16-bit range.
# The maximum value for 16-bit grayscale is 65535 (2^16 - 1).
# We multiply the 8-bit grayscale values (max 255) by 257 (255 * 257 ≈ 65535) to spread the range.
img_gray_16bit = img_gray.point(lambda x: x * 257)

# Save the 16-bit grayscale image
img_gray_16bit.save("gray16_image.png")