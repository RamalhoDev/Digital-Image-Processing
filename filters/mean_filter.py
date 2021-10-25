from .filter import Filter
import numpy as np

class MeanFilter(Filter):

    def evaluate_pixel(self, indexes, line, column):

        new_r = np.multiply(self.image[indexes['begin_line']:indexes['end_line'] + 1, indexes['begin_column']:indexes['end_column'] + 1,0], self.mask).sum()
        new_g = np.multiply(self.image[indexes['begin_line']:indexes['end_line'] + 1, indexes['begin_column']:indexes['end_column'] + 1,1], self.mask).sum()
        new_b = np.multiply(self.image[indexes['begin_line']:indexes['end_line'] + 1, indexes['begin_column']:indexes['end_column'] + 1,2], self.mask).sum()

        return round(new_r), round(new_g), round(new_b)

class MeanFilterY(Filter):

    def evaluate_pixel(self, indexes, line, column):

        new_y = np.multiply(self.image[indexes['begin_line']:indexes['end_line'] + 1, indexes['begin_column']:indexes['end_column'] + 1,0], self.mask).sum()
        
        return new_y, self.image[line,column,1], self.image[line,column,2]

