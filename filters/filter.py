from math import floor
from abc import ABC, abstractmethod
import numpy as np

class Filter(ABC):

    def __init__(self, mask : np.ndarray) -> None:
        self.mask = mask
        self.define_mask_center()
   
    def define_mask_center(self):
        self.m = np.shape(self.mask)[0]
        self.n = np.shape(self.mask)[1]
        self.x_center = floor(self.m/2.0)
        self.y_center = floor(self.n/2.0)

    def set_image(self,image:np.ndarray):
        self.image = image

    def pre_process_indexes(self, line, column):
        begin_line = line - self.x_center + (1 if (self.m % 2) == 0 else 0)
        begin_column = column - self.y_center + (1 if (self.n % 2) == 0 else 0)
        end_line = line + self.x_center
        end_column = column + self.y_center          

        return {"begin_column" : begin_column, "end_column": end_column, "begin_line": begin_line, "end_line":end_line}    


    def correlation(self, offset, scale):
        corr_image = np.ndarray(np.shape(self.image))

        for i in range(np.shape(self.image)[0]):
            for j in range(np.shape(self.image)[1]):
                indexes = self.pre_process_indexes(i,j)
                
                if indexes["begin_line"] < 0 or indexes["begin_column"] < 0:
                    continue
                if indexes["end_line"] >= np.shape(self.image)[0] or indexes["end_column"] >= np.shape(self.image)[1]:
                    continue

                corr_image[i,j,0] = offset + scale * np.multiply(self.mask,self.image[indexes["begin_line"]:indexes["end_line"] + 1, indexes["begin_column"]:indexes["end_column"]+ 1, 0] ).sum()
                corr_image[i,j,1] = offset + scale * np.multiply(self.mask,self.image[indexes["begin_line"]:indexes["end_line"] + 1, indexes["begin_column"]:indexes["end_column"]+ 1, 1] ).sum()
                corr_image[i,j,2] = offset + scale * np.multiply(self.mask,self.image[indexes["begin_line"]:indexes["end_line"] + 1, indexes["begin_column"]:indexes["end_column"]+ 1, 2] ).sum()
        
        return corr_image        
        
    @abstractmethod
    def evaluate_pixel_rgb(self, indexes, line=-1, column=-1):
        pass
    
    def apply_filter_on_image(self):
        new_image = np.ndarray(np.shape(self.image))
        
        for i in range(np.shape(self.image)[0]):
            for j in range(np.shape(self.image)[1]):

                indexes = self.pre_process_indexes(i,j)

                if indexes["begin_line"] < 0 or indexes["begin_column"] < 0:
                    continue
                if indexes["end_line"] >= np.shape(self.image)[0] or indexes["end_column"] >= np.shape(self.image)[1]:
                    continue

                new_image[i,j,0], new_image[i,j,1], new_image[i,j,2] = self.evaluate_pixel_rgb(indexes, i, j)

        return new_image
        