from PIL import Image
from time import time

def color(d):
    return [(255,255,255), (0,0,0), (0,0,255), (0,255,0), (255,0,0)][d]

def save(depth, scale=16):
    w = len(depth[0])
    h = len(depth)

    img = Image.new("RGB", (w,h))

    for y in range(h):
        for x in range(w):
            #(x*3+1,y*3+)
            img.putpixel((x,y), color(depth[y][x]))

    img = img.resize((w*scale,h*scale), Image.NEAREST)
    img.save(f"img/{int(time())}.png")
