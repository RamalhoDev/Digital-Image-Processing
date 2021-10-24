class NegativeFilter():

    def negative_rgb(self, indexes):

            negativeRGB[i,j,0] = 255 - rgb[i,j,0]
            negativeRGB[i,j,1] = 255 - rgb[i,j,1]
            negativeRGB[i,j,2] = 255 - rgb[i,j,2]

        return round(new_r), round(new_g), round(new_b)
