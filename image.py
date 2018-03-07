from PIL import Image

im = Image.open("mario.png")
px = im.load()
#im.rotate(45).show()

def rgb2hex(rgb):
    r,g,b = rgb
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def get_average_color_square(starting_x, starting_y, boxWidth, boxHeight):
	"Takes the NW corner of a box as input, along with sample box height and width, and returns the average hex color for that box"

	sum_r = 0
	sum_g = 0
	sum_b = 0
	counter = 0
	for w_px in range(starting_x, starting_x + boxWidth):
		for h_px in range(starting_y, starting_y + boxHeight):
			#print(rgb2hex((px[w_px,h_px])))
			r,g,b = px[w_px, h_px]
			sum_r += r
			sum_g += g
			sum_b += b
			counter += 1
			#print(px[w_px,h_px])

	return(int(sum_r/counter), int(sum_g/counter), int(sum_b/counter))

def set_color_square(color, starting_x, starting_y, boxWidth, boxHeight):
	"Takes the NW corner of a box as input, along with sample box height and width, and sets the entire box to the (r,g,b) tuple passed in"

	for w_px in range(starting_x, starting_x + boxWidth):
		for h_px in range(starting_y, starting_y + boxHeight):

			px_out[w_px, h_px] = color

	return color

width, height = im.size
print(width,height)
print(im.mode)

im_out = Image.new("RGB", (width, height))
#im_out.save("out.png")

px_out = im_out.load()

#userWidth = input("Width of canvas in Inches: ")
userWidth = 5
#userHeight = input("Height of canvas in Inches: ")
userHeight = 5

boxWidth = 50
boxHeight = 50

width_loops = width / boxWidth
width_remainder = width % boxWidth
height_loops = height / boxHeight
height_remainder = height % boxHeight

print(width_loops, height_loops, width_remainder, height_remainder)

colorlist = []
for w_px in range(int(width_remainder / 2), width,boxWidth):
    for h_px in range(int(height_remainder / 2), height, boxHeight):
        #print(px[w_px,h_px])
        if(w_px + boxWidth < width and h_px + boxHeight < height):
	        print("At w: ", w_px, " h: ", h_px)
	        avg_color = get_average_color_square(w_px,h_px,boxWidth,boxHeight)
	        print("Avg color: ", avg_color)

	        set_color_square(avg_color, w_px, h_px, boxWidth, boxHeight)

	        rgb = px[w_px,h_px]
	        hexvalue = rgb2hex((px[w_px,h_px]))
	        if(hexvalue not in colorlist):
	            colorlist.append(hexvalue)

    #print()
print (colorlist)

im_out.save("out.png")