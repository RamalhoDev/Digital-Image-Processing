from .filter import Filter

class NegativeFilterRGB(Filter):

    def evaluate_pixel(self, indexes, line, column):

        new_r = 255 - self.image[line, column, 0]
        new_g = 255 - self.image[line, column, 1]
        new_b = 255 - self.image[line, column, 2]

        return new_r, new_g, new_b

class NegativeFilterYIQ(Filter):

    def evaluate_pixel(self, indexes, line, column):

        new_y = 255 - self.image[line, column, 0]
        new_i = self.image[line, column, 1]
        new_q = self.image[line, column, 2]

        return new_y, new_i, new_q