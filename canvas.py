from PIL import Image, ImageDraw
import os
import numpy as np
from fragment import *


def get_all_names(name_dir):
    all_names = []
    for filename in os.listdir(name_dir):
        if filename.endswith('.jpg'):
            all_names.append(filename)
    return all_names


class Canvas:
    def __init__(self, name_base_img, count_w=50, count_h=50, base_img=None):
        self.name_base_img = name_base_img
        self.count_w = count_w
        self.count_h = count_h

        if name_base_img is not None:
            with Image.open(name_base_img) as img:
                self.base_img = img
                self.new_img = img.copy()
        else:
            self.base_img = base_img
            self.new_img = base_img.copy()

        self.all_imgs = []
        self.fragments = []

    def load_all_imgs(self, name_dir):
        all_names = get_all_names(name_dir)
        for name in all_names:
            output_path = os.path.join(name_dir, name)
            self.all_imgs.append(Img(output_path))

    def create_fragments(self):
        width, height = self.new_img.size
        w, h = width // self.count_w, height // self.count_h
        x, y = 0, 0

        for i in range(self.count_h):
            for j in range(self.count_w):
                x, y = w * j, h * i
                part = self.base_img.crop((x, y, x+w, y+h))
                self.fragments.append(Fragment(x, y, w, h, part))

    def set_ratings(self):
        n = 0
        for frag in self.fragments:
            n += 1
            if n % 250 == 0:
                print('.', end='')
            frag.set_rating(self.all_imgs)


    def create_result(self):
        for frag in self.fragments:
            frag.create_img()

        width, height = self.new_img.size
        w, h = width // self.count_w, height // self.count_h
        x, y = 0, 0

        for i in range(self.count_h):
            for j in range(self.count_w):
                frag = self.fragments[i * self.count_h + j]
                x, y = w * j, h * i
                self.new_img.paste(frag.get_result(), (x, y))






if __name__ == "__main__":
    name_dir = 'images/processed'
    canvas = Canvas('images/main.jpg')
    canvas.create_fragments()
    canvas.create_result()
    canvas.new_img.save('images/main2.jpg')


