from PIL import Image, ImageDraw
import os
import numpy as np
from img import Img, get_average_colors, fill_img_average_colors


class Fragment:
    def __init__(self, x, y, width, height, start_fragment):
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.img = None
        self.start_fragment = start_fragment
        self.average_color_parts = get_average_colors(start_fragment)
        self.rating = []

    def create_img(self):
        if len(self.rating) == 0:
            new_image = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(new_image)
            fill_img_average_colors(draw, new_image, self.average_color_parts)
            self.img = new_image
        else:
            self.rating.sort(key=lambda x: x.compare(self.average_color_parts))
            self.img = self.rating[0].img
            self.rating[0].used_count += 1

    def set_rating(self, all_imgs):
        all_imgs.sort(key=lambda x: x.compare(self.average_color_parts))
        self.rating.append(all_imgs[0])
        self.rating.append(all_imgs[1])
        self.rating.append(all_imgs[2])




    def get_result(self):
        return self.img

