from PIL import Image
from filters.emboss_filter import EmbossFilter
from filters.mean_filter import MeanFilter, MeanFilterY
from filters.median_filter import MedianFilter, MedianFilterY
from filters.prewitt_filter import PrewittFilter
from filters.negative_filter import NegativeFilterRGB, NegativeFilterYIQ
from tarefas.tarefa6 import reproduce_example_6
import numpy as np
import argparse as ap
import cv2

parser = ap.ArgumentParser(description = "System made for the lecture Processamento Digital de Imagens in UFPB.")
parser.add_argument('image_path', help="Path to the image", type=str)
parser.add_argument('mask_path', help="Path to the mask and filter", type=str)
parser.add_argument('-v','--verbose', help="Enable RGB to YIQ conversion.", action="store_true", default = 0)
parser.add_argument('-s','--stretching', help="Enable histogram stretching.", action="store_true")
parser.add_argument('-y','--yiq_rgb', help="Enable YIQ to RGB conversion.", action="store_true")
parser.add_argument('-r','--rgb_yiq', help="Enable RGB to YIQ conversion.", action="store_true", default = 1)
parser.add_argument('-4', '--test4', help="Run test 4.", action="store_true")
parser.add_argument('-6','--test6', help="Run test 6.", action="store_true")
args = parser.parse_args()

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

def read_mask_from_file(file):
    filter = None
    with open(file, mode='r') as f:
        line = f.read().split(" ")
        mode = line[0]
        m = int(line[1])
        n = int(line[2])
        filter = np.zeros((m, n))
        if mode == "mean":
            filter = filter + (1.0/(m * n))
        elif mode == "emboss":
            if n==3:
                filter = np.array(((-2,-1,0),(-1,1,1),(0,1,2)))
            elif n==5:
                filter = np.array((-2,0,-1,0,0),(0,-2,-1,0,0),(-1,-1,1,1,1),(0,0,1,2,0),(0,0,1,0,2))
            else:
                assert False, f"{m} x {n} emboss filter not implemented yet"
        elif mode == "prewitt":
            if n==3:
                filter = np.zeros((m,n,2))

                filter[0,0,0] = 1
                filter[0,1,0] = 1
                filter[0,2,0] = 1
                filter[2,0,0] = -1
                filter[2,1,0] = -1
                filter[2,2,0] = -1

                filter[0,0,1] = 1
                filter[1,0,1] = 1
                filter[2,0,1] = 1
                filter[0,2,1] = -1
                filter[1,2,1] = -1
                filter[2,2,1] = -1

            else:
                assert False, f"{m} x {n} prewitt filter not implemented yet"
        elif mode == "median":
            filter = np.ones((m, n))
        elif mode == "negative":
            filter = np.ones((1,1))
        else:
            assert False, f"{m} x {n} {mode} filter not implemented yet (maybe a typo in {mode}?) modes supported:\nprewitt, emboss, mean, median\n"
    return filter, mode

def histogram_stretching_y(image : np.ndarray):
    min_value = image[:,:,0].min()
    max_value = image[:,:,0].max()

    new_image = np.copy(image)

    for i in range(np.shape(image)[0]):
        for j in range(np.shape(image)[1]):
            new_image[i,j,0] = round(((image[i,j,0] - min_value)/(max_value - min_value)) * 255)
    
    return new_image

def histogram_stretching(image : np.ndarray):
    min_value_r = image.min()
    max_value_r = image.max()

    new_image = np.copy(image)

    for i in range(np.shape(image)[0]):
        for j in range(np.shape(image)[1]):
            new_image[i,j,0] = round(((image[i,j,0] - min_value_r)/(max_value_r - min_value_r)) * 255)
            new_image[i,j,1] = round(((image[i,j,1] - min_value_r)/(max_value_r - min_value_r)) * 255)
            new_image[i,j,2] = round(((image[i,j,2] - min_value_r)/(max_value_r - min_value_r)) * 255)

    return new_image


image = Image.open(args.image_path).convert("RGB")

pixels = np.array(image)

if args.verbose:
    print("Image:\n", image)


if args.test4:
    pixels_yiq = from_rgb_to_yiq(pixels)
    mask1, _ = read_mask_from_file("masks/mean_1x21.txt")
    mask2, _ = read_mask_from_file("masks/mean_21x1.txt")
    filter = MeanFilterY(mask1)
    filter.set_image(pixels_yiq)

    image_after_filter = filter.apply_filter_on_image()
    pixels_new_image = image_after_filter

    filter2 = MeanFilterY(mask2)
    filter.set_image(pixels_new_image)
    image_after_filter2 = filter.apply_filter_on_image()

    PIL_image = Image.fromarray(image_after_filter2.astype(np.uint8))
    PIL_image.show()    
    exit(3)

if args.test6:
    pixels = cv2.imread(args.image_path)
    mask = cv2.imread(args.mask_path)

    if args.verbose:
        print(mask)
    reproduce_example_6(pixels, mask)
    exit(2)


mask, mode = read_mask_from_file(args.mask_path)

if args.verbose:
    print("Using mask: ", mask)

filter = None
image_after_filter = None
if(args.yiq_rgb):
    pixels = from_rgb_to_yiq(pixels)

if mode == "mean":
    if(args.yiq_rgb):
        filter = MeanFilterY(mask)
    else:
        filter = MeanFilter(mask)
elif mode == "emboss":
    filter = EmbossFilter(mask)
elif mode == "prewitt":
    filter = PrewittFilter(mask)
elif mode == "median":
    filter = MedianFilterY(mask)
elif mode == "negative":
    if(args.yiq_rgb):
        filter = NegativeFilterYIQ(mask)
    else:
        filter = NegativeFilterRGB(mask)

filter.set_image(pixels)
image_after_filter = filter.apply_filter_on_image()

if(args.stretching):
    if(args.yiq_rgb):
        image_after_filter = histogram_stretching_y(image_after_filter)
    else:
        image_after_filter = histogram_stretching(image_after_filter)        

if(args.yiq_rgb):
    image_after_filter = from_yiq_to_rgb(image_after_filter)

PIL_image = Image.fromarray(image_after_filter.astype(np.uint8))
PIL_image.show()


