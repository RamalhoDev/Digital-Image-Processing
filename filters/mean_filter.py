from .filter import Filter

class MeanFilter(Filter):

    def evaluate_pixel_rgb(self, indexes):
        count_line = 0
        new_r, new_g, new_b = (0,0,0)
        width, height = self.image.size

        for i in range(indexes['begin_line'], indexes['end_line'] + 1):
            count_column = 0
            for j in range(indexes['begin_column'], indexes['begin_column'] + 1):
                (r_channel, g_channel, b_channel) = self.data[i * width + j]

                new_r += (r_channel * self.mask[count_line][count_column])
                new_g += (g_channel * self.mask[count_line][count_column])
                new_b += (b_channel * self.mask[count_line][count_column])

                count_column += 1
            count_line += 1

        return round(new_r), round(new_g), round(new_b)
