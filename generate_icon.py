#!/usr/bin/env python3
"""Generate app-icon.ico based on Fleur Airlines fleur-de-lis logo"""
import struct

def create_fleur_ico(output_path):
    """Create ICO with fleur-de-lis logo (gold on navy)"""
    size = 256
    pixels = bytearray(size * size * 4)
    
    # Fill with navy blue background
    for i in range(size * size):
        idx = i * 4
        pixels[idx:idx+4] = bytes([30, 43, 25, 255])  # Navy BGRA
    
    # Draw fleur-de-lis in gold
    cx, cy = size // 2, size // 2
    gold = bytes([80, 205, 245, 255])  # Gold in BGRA
    
    # Main petal (top center)
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            
            # Center vertical petal (top)
            if abs(dx) < 20 and -80 < dy < -20 and dist < 70:
                idx = (y * size + x) * 4
                pixels[idx:idx+4] = gold
            
            # Left petal
            elif (-80 < dx < -30) and (-20 < dy < 40) and (dx*dx + (dy-10)**2) < 1600:
                idx = (y * size + x) * 4
                pixels[idx:idx+4] = gold
            
            # Right petal
            elif (30 < dx < 80) and (-20 < dy < 40) and (dx*dx + (dy-10)**2) < 1600:
                idx = (y * size + x) * 4
                pixels[idx:idx+4] = gold
            
            # Lower left petal
            elif (-60 < dx < -10) and (40 < dy < 100) and ((dx+30)**2 + (dy-60)**2) < 1800:
                idx = (y * size + x) * 4
                pixels[idx:idx+4] = gold
            
            # Lower right petal
            elif (10 < dx < 60) and (40 < dy < 100) and ((dx-30)**2 + (dy-60)**2) < 1800:
                idx = (y * size + x) * 4
                pixels[idx:idx+4] = gold
            
            # Center stem
            elif abs(dx) < 12 and 20 < dy < 80:
                idx = (y * size + x) * 4
                pixels[idx:idx+4] = gold
    
    bmp_data = create_bmp(size, size, bytes(pixels))
    
    # Create ICO header
    ico_data = bytearray()
    ico_data += struct.pack('<HHH', 0, 1, 1)  # Reserved, Type, Count
    
    # Image directory entry
    ico_data += struct.pack('<BBBBHHII',
        size, size, 0, 0, 1, 32,
        len(bmp_data),
        22)
    
    # Add BMP data (skip file header)
    ico_data += bmp_data[14:]
    
    with open(output_path, 'wb') as f:
        f.write(ico_data)
    
    print(f"✓ Created {output_path}")

def create_bmp(width, height, pixel_data):
    """Create BMP file data"""
    row_size = ((width * 32 + 31) // 32) * 4
    data_size = row_size * height
    file_size = 14 + 40 + data_size
    
    # BMP file header
    bmp = struct.pack('<H', 0x4D42)  # 'BM'
    bmp += struct.pack('<I', file_size)
    bmp += struct.pack('<I', 0)  # Reserved
    bmp += struct.pack('<I', 54)  # Offset to pixel data
    
    # DIB header (BITMAPINFOHEADER)
    bmp += struct.pack('<I', 40)  # Header size
    bmp += struct.pack('<i', width)
    bmp += struct.pack('<i', height)
    bmp += struct.pack('<H', 1)   # Planes
    bmp += struct.pack('<H', 32)  # Bits per pixel
    bmp += struct.pack('<I', 0)   # Compression
    bmp += struct.pack('<I', data_size)
    bmp += struct.pack('<i', 0)   # X pixels per meter
    bmp += struct.pack('<i', 0)   # Y pixels per meter
    bmp += struct.pack('<I', 0)   # Colors used
    bmp += struct.pack('<I', 0)   # Important colors
    
    # Pixel data (BMP is bottom-up)
    for y in range(height - 1, -1, -1):
        row = pixel_data[y * width * 4:(y + 1) * width * 4]
        bmp += row
        # Padding
        padding = row_size - (width * 4)
        if padding > 0:
            bmp += b'\x00' * padding
    
    return bmp

if __name__ == '__main__':
    import os
    os.makedirs('src/main/resources', exist_ok=True)
    create_simple_ico('src/main/resources/app-icon.ico')
