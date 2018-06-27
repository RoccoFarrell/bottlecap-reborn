#Bottlecap.io Reborn - CapCollage.io

##Overview

A utility for generating bottlecap tables from images

##Dependencies
Scikit-image
	_pip install scikit-image_
Scikit-learn
	_pip install scikit-image_
Python 3.6

I would just run `pip install` for any errors you get of failed packages

##To Use
Copy your original image to the `images` folder in the project
Open `image.py` and change the line `infile = img_dir + "corey.png"` to change which file is transformed
You can also modify `num_colors` and `boxWidth = boxHeight = <x>` to play with the number of colors in the image, and the size of the pixels in the output image
Navigate to the root directory and run `python image.py` to process the image that you specified above
