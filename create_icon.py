#!/usr/bin/env python3
import struct, zlib, os

def write_bmp_icon(path, size, bg_color, accent_color):
    """Generate a simple BMP icon file"""
    w, h = size, size
    # BMP file format (24-bit)
    pixel_data = bytearray()
    for y in range(h):
        row = bytearray()
        for x in range(w):
            # Mix colors in center
            dx = x - w//2
            dy = y - h//2
            dist = (dx*dx + dy*dy) ** 0.5
            
            if dist < w//4:
                # Center: accent color
                row.extend(accent_color)
            else:
                # Background
                row.extend(bg_color)
        
        # BMP requires rows padded to 4-byte boundary
        padding = (4 - (w * 3) % 4) % 4
        row.extend(b'\x00' * padding)
        pixel_data = row + pixel_data  # BMP is upside down
    
    # BMP Header (14 bytes)
    file_size = 14 + 40 + len(pixel_data)
    bmp_header = struct.pack('<HHIIIHH', 
        0x4D42,  # Signature 'BM'
        file_size & 0xFFFF,
        (file_size >> 16) & 0xFFFF,
        0, 0,
        14 + 40,  # Offset to pixel data
        40)
    
    # DIB Header (40 bytes)
    dib_header = struct.pack('<IHHIIHHHH',
        40,  # Header size
        w, h,
        1,  # Planes
        24,  # Bits per pixel
        0, 0, 0, 0, 0, 0)
    
    with open(path, 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header)
        f.write(pixel_data)

def create_ico_from_png(png_path, ico_path, sizes=[16, 32, 48, 64, 128, 256]):
    """Convert PNG to ICO using PIL if available, else create a simple BMP ICO"""
    try:
        from PIL import Image
        # Try to load and resize
        img = Image.open(png_path)
        images = []
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Save as ICO (PIL handles multiple sizes)
        images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes])
        print(f"Created {ico_path} with PIL")
    except:
        # Fallback: create a simple BMP-based ICO
        # For simplicity, we'll create a minimal ICO with one 256x256 entry
        bg = bytes([15, 43, 92])    # Navy blue
        accent = bytes([245, 205, 80])  # Gold
        
        # Create temporary BMP
        temp_bmp = ico_path.replace('.ico', '.bmp')
        write_bmp_icon(temp_bmp, 256, bg, accent)
        
        # Read BMP data
        with open(temp_bmp, 'rb') as f:
            bmp_data = f.read()
        
        # ICO header (simple format with 1 image)
        ico_header = struct.pack('<HHH', 0, 1, 1)
        img_dir = struct.pack('<BBBBHHII', 
            256, 256,  # width, height
            0, 0,  # colors, reserved
            1, 24,  # planes, bits per pixel
            len(bmp_data) - 54,  # image size (skip BMP headers)
            22)  # offset to image data in ICO
        
        with open(ico_path, 'wb') as f:
            f.write(ico_header)
            f.write(img_dir)
            f.write(bmp_data[54:])  # Skip BMP headers
        
        os.remove(temp_bmp)
        print(f"Created {ico_path} (fallback format)")

# Create icon
os.makedirs('src/main/resources', exist_ok=True)
create_ico_from_png('src/main/resources/app-icon.ico', 'src/main/resources/app-icon.ico')
print("Icon created successfully!")
