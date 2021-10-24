from .filter import Filter

class MeanFilter(Filter):

    def evaluate_pixel_rgb(self, indexes):
        count_line = 0
        new_r, new_g, new_b = (0,0,0)

        for i in range(indexes['begin_line'], indexes['end_line'] + 1):
            count_column = 0
            for j in range(indexes['begin_column'], indexes['end_column'] + 1):
                new_r += self.image[i,j,0] * self.mask[count_line,count_column]
                new_g += self.image[i,j,1] * self.mask[count_line,count_column]
                new_b += self.image[i,j,2] * self.mask[count_line,count_column]

                count_column += 1
            count_line += 1

        return round(new_r), round(new_g), round(new_b)
