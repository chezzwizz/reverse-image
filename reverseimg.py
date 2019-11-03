import struct
from sys import argv as args

# Set the header key
header_fmtstr = "<ccihhiiIIhhiiIIii"
# Bitmap header information:
#   Offset  |   Size (bytes)   |   Purpose/Note
# ==========+==================+================================================
#    0x00   |       2          |   Identification  or header field used to
#           | (2 x 8bit char)  |   determine if it is a bitmap. This field
#           |                  |   should always be 'BM' for Windows BMP files.
# ----------+------------------+------------------------------------------------
#    0x02   |       4          |   The size in bytes of the file. 4,294,927,296
#           |   (32bit int)    |   bytes theoretical maximum size. (~3.95GB)
# ----------+------------------+------------------------------------------------
#    0x06   |       2          |   Reserved: Application dependant.
#           |  (16bit short)   |
# ----------+------------------+------------------------------------------------
#    0x08   |       2          |   Reserved: Application dependant.
#           |  (16bit short)   |
# ----------+------------------+------------------------------------------------
#    0x0A   |       4          |   The starting address of the pixel data. The
#           |   (32bit int)    |   data array size can be calculated using the
#           |                  |   width, height, and color depth or bits per
#           |                  |   pixel (bpp). Most bitmaps are 1, 8, 16, 24 or
#           |                  |   32 bits.
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#    The following header information is specific to the Windows bitmap format.
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#    0x0E   |       4          |   The size of the header data in bytes.
#           |   (32bit int)    |
# ----------+------------------+------------------------------------------------
#    0x12   |       4          |   The width of the bitmap as a signed integer.
#           |(32bit signed int)|
# ----------+------------------+------------------------------------------------
#    0x16   |       4          |   The heigh of the bitmap as a signed integer.
#           |(32bit signed int)|
# ----------+------------------+------------------------------------------------
#    0x1A   |       2          |   The number of color planes. This field will
#           |  (16bit short)   |   always be 1 for Windows bitmaps.
# ----------+------------------+------------------------------------------------
#    0x1C   |       2          |   BPP or color depth. This field determines the
#           |  (16bit short)   |   rang of colors the bitmap color pallet.
# ----------+------------------+------------------------------------------------
#    0x1E   |       4          |   Compression method used to reduce the overall
#           |   (32bit int)    |   file size. There are several possible
#           |                  |   compression types, but more commonly, there
#           |                  |   will be no compression and the value will be
#           |                  |   0.
# ----------+------------------+------------------------------------------------
#    0x22   |       4          |   The size of the raw bitmap data in bytes.
#           |   (32bit int)    |   This field may also be set 0 for the most
#           |                  |   common type of uncompressed bitmap file.
# ----------+------------------+------------------------------------------------
#    0x26   |       4          |   The pixel resolution of the image on the
#           |(32bit signed int)|   horizontal dimension. This field indicates
#           |                  |   the number of pixels pre metre as a signed
#           |                  |   integer.
# ----------+------------------+------------------------------------------------
#    0x2A   |       4          |   The pixel resolution of the image on the
#           |(32bit signed int)|   vertical dimension. This field indicates the
#           |                  |   number of pixels per metre as a signed
#           |                  |   integer.
# ----------+------------------+------------------------------------------------
#    0x2E   |       4          |   This field is the number of colors used in
#           |   (32bit int)    |   the image or the images color palette. This
#           |                  |   field can also be set to 0 to indicate that
#           |                  |   the number of colors defaults to 2 raised to
#           |                  |   the power of the bpp.
# ----------+------------------+------------------------------------------------
#    0x32   |       4          |   This field is a number of important colors
#           |   (32bit int)    |   in the image or 0 for all colors.
# ----------+------------------+------------------------------------------------
#    0x36   |  This is the start of the raw pixel data and all the data past
#           |  this point represents each pixel as determined by the color
#           |  depth. The length of this field is determined by calculating the
#           |  number of pixels in each row times the height of the image.
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

file = args[1] # Read the filename from the command line

# Open the file in binary mode for read write operations and get the pixel data
img = open(file, 'r+b')
header = struct.unpack_from(header_fmtstr, img.read(54))
pixels = bytes()

# The 6th index in the header key tells us where to start reading and writing
# pixels.
img.seek(header[5])

# Loop through the pixels and reverse the bit 
for byt in img.read(header[12]):
  pixels += int.to_bytes(255 - byt, 1, 'little')

img.seek(header[5])
img.write(pixels)
img.close()
