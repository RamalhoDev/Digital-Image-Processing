from .filter import Filter
import numpy as np

class MeanFilterY(Filter):

    def evaluate_pixel_rgb(self, indexes, line, column):

        new_y = np.multiply(self.image[indexes['begin_line']:indexes['end_line'] + 1, indexes['begin_column']:indexes['end_column'] + 1,0], self.mask).sum()
        
        return new_y, self.image[line,column,1], self.image[line,column,2]
