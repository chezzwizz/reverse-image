import struct
from sys import argv as args

# Set the header key
# Uses a Microsoft Windows(TM) specific format.
header_fmtstr = "<ccihhiiIIhhiiIIii"

file = args[1] # Read the filename from the command line

# Open the file in binary mode for read write operations and get the pixel data
img = open(file, 'r+b')
header = struct.unpack_from(header_fmtstr, img.read(54))
pixels = bytes()

# The header data at index 5 tells us the header length.
# Here we move the cursor to the end of the header data.
img.seek(header[5])

# Loop through the pixels and reverse the bit 
for byt in img.read(header[12]):
  pixels += int.to_bytes(255 - byt, 1, 'little')

# Since we moved the cursor to read the pixels, we need to reset the cursor
# position and write the next pixel data.
img.seek(header[5])
img.write(pixels)
img.close()
