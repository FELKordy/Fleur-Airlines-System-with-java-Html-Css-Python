import zlib, struct, os
os.makedirs('src/main/resources/images', exist_ok=True)

def write_png(path, width, height, pixels):
    def png_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('!I', len(data)) + chunk + struct.pack('!I', zlib.crc32(chunk) & 0xffffffff)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        ihdr = struct.pack('!IIBBBBB', width, height, 8, 6, 0, 0, 0)
        f.write(png_chunk(b'IHDR', ihdr))
        scanlines = b''
        stride = width * 4
        for y in range(height):
            scanlines += b'\x00' + pixels[y*stride:(y+1)*stride]
        f.write(png_chunk(b'IDAT', zlib.compress(scanlines, 9)))
        f.write(png_chunk(b'IEND', b''))

def gradient(width, height, c1, c2):
    data = bytearray(width * height * 4)
    for y in range(height):
        t = y / (height - 1)
        r = int(c1[0] * (1-t) + c2[0] * t)
        g = int(c1[1] * (1-t) + c2[1] * t)
        b = int(c1[2] * (1-t) + c2[2] * t)
        for x in range(width):
            idx = (y * width + x) * 4
            data[idx:idx+4] = bytes((r,g,b,255))
    return bytes(data)

def draw_circle(pixels, width, height, cx, cy, r, col):
    pixels = bytearray(pixels)
    for y in range(height):
        for x in range(width):
            if (x-cx)**2+(y-cy)**2 <= r*r:
                i = (y*width+x)*4
                pixels[i:i+4] = bytes(col)
    return bytes(pixels)

def draw_fleur(pixels, width, height):
    pixels = bytearray(pixels)
    mid = width//2
    base_y = height//2 + 10
    for y in range(height):
        for x in range(width):
            dx=x-mid
            dy=y-base_y
            if dy<0 and abs(dx) < 20 - dy//3 and abs(dx) > 5 + dy//6:
                i=(y*width+x)*4
                pixels[i:i+4]=bytes((245,205,80,255))
            if dy<18 and abs(dx)<8:
                i=(y*width+x)*4
                pixels[i:i+4]=bytes((245,205,80,255))
    return bytes(pixels)

w,h = 300,150
bg = gradient(w,h,(15,43,92),(7,33,74))
logo = draw_fleur(bg, w, h)
logo = draw_circle(logo, w,h, w//2, 38, 12, (255,255,255,120))
write_png('src/main/resources/images/logo.png', w, h, logo)

for name, c1, c2, label in [
    ('paris.png',(25,58,88),(26,129,146),'PARIS'),
    ('athens.png',(45,71,110),(36,106,149),'ATHENS'),
    ('dubai.png',(20,56,100),(32,149,164),'DUBAI')
]:
    w,h = 420,240
    bg = gradient(w,h,c1,c2)
    bg = draw_circle(bg,w,h, w//2, h//2, 70, (255,255,255,40))
    bg = draw_circle(bg,w,h, w//2+80, h//2-30, 40, (255,255,255,30))
    pixels = bytearray(bg)
    for y in range(30,90):
        for x in range(40,380):
            i=(y*w+x)*4
            r,g,b,a = pixels[i:i+4]
            pixels[i:i+4]=bytes((min(255,r+15),min(255,g+15),min(255,b+15),a))
    tx = 50
    for ch in label:
        if ch == ' ':
            tx += 20
            continue
        for dx in range(10):
            for dy in range(30):
                for px in range(8):
                    x = tx + dx*2 + px
                    y = 40 + dy
                    if x < w and y < h:
                        i=(y*w+x)*4
                        pixels[i:i+4]=bytes((255,255,255,255))
        tx += 20
    write_png(f'src/main/resources/images/{name}', w, h, bytes(pixels))
print('created files')
