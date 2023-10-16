import cv2

def is_png(imgfile):  # Verify image is a PNG or not
  with open(imgfile, 'rb') as file:
    first5bytes = file.read(5)
  return (first5bytes == b'\x89PNG\r')

def compress_png_to_jpeg(source_png_image, compressed_jpeg_image, jpeg_quality):  # Compress PNG to JPEG
  if (not is_png(source_png_image)):
    raise ValueError("Not a PNG image.")
  image = cv2.imread(source_png_image)
  if (compressed_jpeg_image[-5::] not in [".jpeg", ".jpg", ".JPEG", ".JPG"]):
    compressed_jpeg_image+=".jpeg"
  cv2.imwrite(compressed_jpeg_image, image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])