from PIL import Image
import numpy as np
from sklearn import cluster
import scipy.misc as FILE
import imageio
import matplotlib.pyplot as plt
from skimage import color
import time

#############################################
#Function Defs
#############################################
def quantize(raster, n_colors):
    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = cluster.KMeans(n_clusters=n_colors)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    return quantized_raster

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

			try:
				px_out[w_px, h_px] = color
			except IndexError:
				print("Error, tried to set color of non-existent pixel")
				print("w: ", int(width_loops * boxWidth), "h: ", int(height_loops * boxHeight))
				print("w_px: ", w_px, "h_px: ", h_px)
				break

	return color

def get_color_list():
	"Returns a list of every hex color in the picture"
	
	colorlist = []
	for w_px in range(1, width):
		for h_px in range(1, height):

			#Get list of colors in original image
			rgb = px[w_px,h_px]
			#hexvalue = rgb2hex((px[w_px,h_px]))
			if(rgb not in colorlist):
				colorlist.append(rgb)
				#print(len(colorlist))

	return colorlist

def find_closest_color(inputcolor, colorlist):
	"Takes in a source color, and a color list, and returns the closest color from the list"

	#print(inputcolor, colorlist)

	r1,g1,b1 = inputcolor
	outputcolor = (0,0,0)

	distance = 1000000
	for color in colorlist:
		r2,g2,b2 = color

		distance_new = float((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)**(1/2.0)
		#print(distance_new)
		#print(r1,r2,g1,g2,b1,b2)

		if(distance_new < distance):
			distance = distance_new
			outputcolor = color

	return outputcolor

#############################################
#Main Program
#############################################
num_colors = 5

img_dir = "../../images/"
infile = img_dir + "mattface.png"


raster = FILE.imread(infile, mode='RGB')
print("read complete")
#print(type(raster))
#print(raster.shape)

#raster2 = imageio.imread('images/tux.png')
#print(type(raster2))
#print(raster2.shape)

#w_in, h_in, depth_in = raster.shape

#if(depth_in == 4):
#	raster = np.reshape(raster, (w_in, h_in, 3))

lab_raster = color.rgb2lab(raster)
print("rgb2lab complete")

start_time = time.time()
output_raster = quantize(lab_raster, num_colors)
print("quantization complete")
print("Quantization took ", (time.time() - start_time))

rgb_raster = (color.lab2rgb(output_raster) * 255).astype('uint8')
print("lab2rgb complete")

FILE.imsave(img_dir + 'quantized.png', rgb_raster)
print("output complete")

#plt.imshow(rgb_raster / 255.0)
#plt.draw()
#plt.show()

im = Image.open(img_dir + 'quantized.png')
px = im.load()

#get W and H
width, height = im.size
print("Size of original: ", width, "x", height)
print("Color mode of original:", im.mode)

#userWidth = input("Width of canvas in Inches: ")
userWidth = 5
#userHeight = input("Height of canvas in Inches: ")
userHeight = 5

#Size of sampling box in pixels
boxWidth = boxHeight = 15

#Find number of loops, and the remainder
width_loops = int(width / boxWidth)
width_remainder = width % boxWidth
height_loops = int(height / boxHeight)
height_remainder = height % boxHeight

print("Total caps: ", width_loops * height_loops)
print("Caps across: ", width_loops)
print("Caps top to bottom: ", height_loops)
print("Projected actual width: ", (width_loops * 1.17)/12, "ft")
print("Projected actual height: ", (height_loops * 1.17)/12, "ft")

#print(width_loops, width_remainder, height_loops, height_remainder)

im_out = Image.new("RGB", (int(width_loops * boxWidth), int(height_loops * boxHeight)))
px_out = im_out.load()

#print((int(width_loops * boxWidth), int(height_loops * boxHeight)))
#print(width_loops, height_loops, width_remainder, height_remainder)

colorlist = get_color_list()

for w_px in range(int(width_remainder / 2), width, boxWidth):
	for h_px in range(int(height_remainder / 2), height, boxHeight):
		#print(px[w_px,h_px])
		if(w_px + boxWidth < int(width_loops * boxWidth) + 1 and h_px + boxHeight < int(height_loops * boxHeight) + 1):
	        #print("At w: ", w_px, " h: ", h_px)

	        #Get average color of a square
			avg_color = get_average_color_square(w_px,h_px,boxWidth,boxHeight)
			#Find closest color
			set_color = find_closest_color(avg_color, colorlist)
			#Set square to that color
			set_color_square(set_color, w_px, h_px, boxWidth, boxHeight)
	
		#else:
			#print("skipping box at ", w_px, h_px, "due to equation")

#print(colorlist)

im_out.save(img_dir + "out.png")

print("done")