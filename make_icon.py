import struct
import os

size = 256
pixels = bytearray(size * size * 4)

# Navy blue background
for i in range(size * size):
    idx = i * 4
    pixels[idx:idx+4] = bytes([30, 43, 25, 255])

# Gold color
gold = bytes([80, 205, 245, 255])
cx, cy = size // 2, size // 2

# Draw fleur-de-lis
for y in range(size):
    for x in range(size):
        dx, dy = x - cx, y - cy
        dist = (dx*dx + dy*dy) ** 0.5
        
        if abs(dx) < 20 and -80 < dy < -20 and dist < 70:
            idx = (y * size + x) * 4
            pixels[idx:idx+4] = gold
        elif (-80 < dx < -30) and (-20 < dy < 40) and (dx*dx + (dy-10)**2) < 1600:
            idx = (y * size + x) * 4
            pixels[idx:idx+4] = gold
        elif (30 < dx < 80) and (-20 < dy < 40) and (dx*dx + (dy-10)**2) < 1600:
            idx = (y * size + x) * 4
            pixels[idx:idx+4] = gold
        elif (-60 < dx < -10) and (40 < dy < 100) and ((dx+30)**2 + (dy-60)**2) < 1800:
            idx = (y * size + x) * 4
            pixels[idx:idx+4] = gold
        elif (10 < dx < 60) and (40 < dy < 100) and ((dx-30)**2 + (dy-60)**2) < 1800:
            idx = (y * size + x) * 4
            pixels[idx:idx+4] = gold
        elif abs(dx) < 12 and 20 < dy < 80:
            idx = (y * size + x) * 4
            pixels[idx:idx+4] = gold

# Create BMP
row_size = ((size * 32 + 31) // 32) * 4
data_size = row_size * size
file_size = 14 + 40 + data_size

bmp = struct.pack('<H', 0x4D42)
bmp += struct.pack('<I', file_size)
bmp += struct.pack('<I', 0)
bmp += struct.pack('<I', 54)
bmp += struct.pack('<I', 40)
bmp += struct.pack('<i', size)
bmp += struct.pack('<i', size)
bmp += struct.pack('<H', 1)
bmp += struct.pack('<H', 32)
bmp += struct.pack('<I', 0)
bmp += struct.pack('<I', data_size)
bmp += struct.pack('<i', 0)
bmp += struct.pack('<i', 0)
bmp += struct.pack('<I', 0)
bmp += struct.pack('<I', 0)

for y in range(size - 1, -1, -1):
    row = pixels[y * size * 4:(y + 1) * size * 4]
    bmp += row
    padding = row_size - (size * 4)
    if padding > 0:
        bmp += b'\x00' * padding

# Create ICO with correct format for 256x256
ico_data = bytearray()
ico_data += struct.pack('<HHH', 0, 1, 1)
# For 256x256, use 0 instead of 256 in ICO dir entry
ico_data += struct.pack('<BBBBHHII', 0, 0, 0, 0, 1, 32, len(bmp), 22)
ico_data += bmp[14:]

os.makedirs('src/main/resources', exist_ok=True)
with open('src/main/resources/app-icon.ico', 'wb') as f:
    f.write(ico_data)

print("✓ Icon created: src/main/resources/app-icon.ico")
