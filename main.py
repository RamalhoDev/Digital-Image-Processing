from PIL import Image
from filters.mean_filter import MeanFilter
from filters.median_filter import MedianFilter

def from_rgb_to_yiq(rgb):
    y = [(0.299 * r + 0.587 * g + 0.114 * b) for (r,g,b) in rgb]
    i = [(0.596 * r - 0.274 * g - 0.322 * b) for (r,g,b) in rgb]
    q = [(0.211 * r - 0.523 * g + 0.312 * b) for (r,g,b) in rgb]

    return list(zip(y,i,q))

def from_yiq_to_rgb(yiq):
    r = [round(1 * y + 0.956 * i + 0.621 * q) for (y,i,q) in yiq]
    g = [round(1 * y - 0.272 * i - 0.647 * q) for (y,i,q) in yiq]
    b = [round(1 * y - 1.106 * i + 1.703 * q) for (y,i,q) in yiq]

    r = [min(max(value, 0), 255) for value in r]
    g = [min(max(value, 0), 255) for value in g]
    b = [min(max(value, 0), 255) for value in b]

    return list(zip(r,g,b))

def read_filter_from_file(file):
    filter = []

    with open(file, mode='r') as f:
        for line in f:
            filter.append([float(line) for line in line.strip().split(' ')])
    
    return filter


image = Image.open("Trabalhos-20211014/Woman.png").convert("RGB")
pixels = image.getdata()

mask = read_filter_from_file("teste.txt")

filter = MedianFilter(mask)

filter.set_image(image)

image_after_filter = filter.apply_filter_on_image()

image_after_filter.show()

