from .filter import Filter
import numpy as np
class MedianFilter(Filter):

	def evaluate_pixel_rgb(self, indexes, line, column):
		new_r = np.median(self.image[indexes['begin_line']:indexes['end_line'] +1,indexes["begin_column"]:indexes["end_column"] + 1, 0])
		new_g = np.median(self.image[indexes['begin_line']:indexes['end_line'] +1,indexes["begin_column"]:indexes["end_column"] + 1, 1])
		new_b = np.median(self.image[indexes['begin_line']:indexes['end_line'] +1,indexes["begin_column"]:indexes["end_column"] + 1, 2])

		return new_r, new_g, new_b

class MedianFilterY(Filter):

	def evaluate_pixel_rgb(self, indexes, line, column):
		new_y = np.median(self.image[indexes['begin_line']:indexes['end_line'] +1,indexes["begin_column"]:indexes["end_column"] + 1, 0])

		return new_y, self.image[line,column, 1], self.image[line,column,2]

