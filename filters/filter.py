from math import floor
from abc import ABC, abstractmethod

class Filter(ABC):

    def __init__(self, mask) -> None:
        self.mask = mask
        self.define_mask_center()
   
    def define_mask_center(self):
        self.m = len(self.mask)
        self.n = len(self.mask[0])
        self.x_center = floor(len(self.mask)/2.0)
        self.y_center = floor(len(self.mask[0])/2.0)

    def set_image(self,image):
        self.image = image
        self.data = list(self.image.getdata())

    def pre_process_indexes(self, pixel_position):
        width, height = self.image.size
        line = floor(pixel_position/width)
        column = pixel_position % width
        begin_line = max(line - self.x_center + (1 if (len(self.mask) % 2) == 0 else 0), 0)
        begin_column = max(column - self.y_center + (1 if (len(self.mask[0]) % 2) == 0 else 0), 0)
        end_line = min(line + self.x_center, height - 1)
        end_column = min(column + self.y_center, width - 1)          

        return {"begin_column" : begin_column, "end_column": end_column, "begin_line": begin_line, "end_line":end_line}    

    @abstractmethod
    def evaluate_pixel_rgb(self, indexes):
        pass
    
    def apply_filter_on_image(self):
        
        new_image = [self.evaluate_pixel_rgb(self.pre_process_indexes(indx)) for indx in range(len(self.data))]
        self.image.putdata(new_image)

        return self.image
        