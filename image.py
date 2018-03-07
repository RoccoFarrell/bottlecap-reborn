from PIL import Image

im = Image.open("mario.png")
px = im.load()
#im.rotate(45).show()

def rgb2hex(rgb):
    r,g,b = rgb
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


width, height = im.size
print(width,height)

colorlist = []
for w_px in range(1,width):
    for h_px in range(1,height):
        #print(px[w_px,h_px])
        rgb = px[w_px,h_px]
        hexvalue = rgb2hex((px[w_px,h_px]))
        if(hexvalue not in colorlist):
            colorlist.append(hexvalue)
    #print()
print (colorlist)
