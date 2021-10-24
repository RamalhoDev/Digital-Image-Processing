from PIL import Image
from filters.mean_filter import MeanFilter
import numpy as np

def from_rgb_to_yiq(rgb: np.ndarray):
    yiq = np.ndarray(np.shape(rgb))

    for i in range(np.shape(yiq)[0]):
        for j in range(np.shape(yiq)[1]):
                
                 yiq[i,j,0] = 0.299 * rgb[i,j,0] + 0.587 * rgb[i,j,1] + 0.114 * rgb[i,j,2]
                 yiq[i,j,1] = 0.596 * rgb[i,j,0] - 0.274 * rgb[i,j,1] - 0.322 * rgb[i,j,2]
                 yiq[i,j,2] = 0.211 * rgb[i,j,0] - 0.523 * rgb[i,j,1] + 0.312 * rgb[i,j,2]

    return yiq

def from_yiq_to_rgb(yiq: np.ndarray):
    rgb = np.ndarray(np.shape(yiq))

    for i in range(np.shape(yiq)[0]):
        for j in range(np.shape(yiq)[1]):    
    
            rgb[i,j,0] = min(max(round(1 * yiq[i,j,0] + 0.956 * yiq[i,j,1] + 0.621 * yiq[i,j,2]),0),255)
            rgb[i,j,1] = min(max(round(1 * yiq[i,j,0] - 0.272 * yiq[i,j,1] - 0.647 * yiq[i,j,2]),0),255)
            rgb[i,j,2] = min(max(round(1 * yiq[i,j,0] - 1.106 * yiq[i,j,1] + 1.703 * yiq[i,j,2]),0),255)

    return rgb

def read_filter_from_file(file):
    with open(file, mode='r') as f:
        for line in f:
            arguments = [line for line in line.strip().split(' ')]
            m = int(arguments[1])
            n = int(arguments[2])
            filter = np.zeros((m, n))
            filter = filter + (1.0/(m * n))
            return filter

def histogram_stretching(image : np.ndarray):
    min_value = image[:,:,0].min()
    max_value = image[:,:,0].max()

    new_image = image

    for i in range(np.shape(image)[0]):
        for j in range(np.shape(image)[1]):
            new_image[i,j,0] = round(((image[i,j,0] - min_value)/(max_value - min_value)) * 255)
    
    return new_image


image = Image.open("Trabalhos-20211014/Woman.png").convert("RGB")

pixels = np.array(image)

mask = read_filter_from_file("teste.txt")

filter = MeanFilter(mask)

filter.set_image(pixels)

image_after_filter = filter.apply_filter_on_image()

yiq = from_rgb_to_yiq(image_after_filter)

image_after_filter = histogram_stretching(yiq)

image_after_filter = from_yiq_to_rgb(image_after_filter)

PIL_image = Image.fromarray(image_after_filter.astype(np.uint8))

PIL_image.show()
