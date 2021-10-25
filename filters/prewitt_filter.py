from math import sqrt
from .filter import Filter
import numpy as np

class PrewittFilter(Filter):

	def evaluate_pixel_rgb(self, indexes, line, column):
		r_horizontal = 0
		r_vertical = 0
		g_horizontal = 0
		g_vertical = 0
		b_horizontal = 0
		b_vertical = 0

		# r_horizontal = np.multiply(self.image[indexes['begin_line']:indexes['end_line']+1,indexes['begin_column']:indexes['end_column']+1, 0], self.mask[:,:,0]).sum()
		r_vertical = np.multiply(self.image[indexes['begin_line']:indexes['end_line']+1,indexes['begin_column']:indexes['end_column']+1, 0], self.mask[:,:,1]).sum()

		# g_horizontal = np.multiply(self.image[indexes['begin_line']:indexes['end_line']+1,indexes['begin_column']:indexes['end_column']+1, 1], self.mask[:,:,0]).sum()
		g_vertical = np.multiply(self.image[indexes['begin_line']:indexes['end_line']+1,indexes['begin_column']:indexes['end_column']+1, 1], self.mask[:,:,1]).sum()
		
		# b_horizontal = np.multiply(self.image[indexes['begin_line']:indexes['end_line']+1,indexes['begin_column']:indexes['end_column']+1, 2], self.mask[:,:,0]).sum()
		b_vertical = np.multiply(self.image[indexes['begin_line']:indexes['end_line']+1,indexes['begin_column']:indexes['end_column']+1, 2], self.mask[:,:,1]).sum()

		new_r = abs(r_vertical) + abs(r_horizontal)
		new_g = abs(g_vertical) + abs(g_horizontal)
		new_b = abs(b_vertical) + abs(b_horizontal)

		return new_r, new_g, new_b