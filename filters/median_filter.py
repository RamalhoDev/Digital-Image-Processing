from .filter import Filter
from math import floor, ceil
class MedianFilter(Filter):

	def evaluate_pixel_rgb(self, indexes):
		count_line = 0
		new_r, new_g, new_b = (0,0,0)
		width, height = self.image.size
		new_r = []
		new_g = []
		new_b = []
		for i in range(indexes['begin_line'], indexes ['end_line'] + 1):
			count_column = 0
			for j in range(indexes['begin_column'], indexes['begin_column'] + 1):
				(r_channel, g_channel, b_channel) = self.data[i * width + j]
				new_r.append(r_channel)
				new_g.append(g_channel)
				new_b.append(b_channel)

				count_column += 1
			count_line += 1
		new_r.sort()
		new_g.sort()
		new_b.sort()
		if (count_line*count_column)%2 != 0:
			pos = floor((count_line*count_column)/2)
			return new_r[pos], new_g[pos], new_b[pos]
		else:
			pos1 = floor((count_line*count_column)/2)
			pos2 = ceil((count_line*count_column)/2)
			return round((new_r[pos1]+new_r[pos2])/2), round((new_g[pos1]+new_g[pos2])/2), round((new_b[pos1]+new_b[pos2])/2)
