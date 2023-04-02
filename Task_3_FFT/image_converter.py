import sys
import numpy as np
from PIL import Image, ImageOps

def get_image_dimensions(image_filename : str):
    image = Image.open(image_filename)
    width, height = image.size
    return width, height

def convert_color_to_grayscale(image_filename: str):
    image = Image.open(image_filename)
    image_grayscale = ImageOps.grayscale(image)
    return image_grayscale

def convert_image_to_hex_array(image_filename : str):
    image = Image.open(image_filename)
    image_grayscale = ImageOps.grayscale(image)
    data = np.asarray(image_grayscale)
    
    original_stdout = sys.stdout

    #with open(array_filename, "w") as array_file:
    #    sys.stdout = array_file
    #    for i in range(len(data)):
    #        for j in range(len(data[i])):
    #            print(data[i][j], end=' ')
    #        if i != len(data) - 1:
    #            print('')
    
    sys.stdout = original_stdout
    
    return data