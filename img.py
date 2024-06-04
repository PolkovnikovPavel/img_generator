from PIL import Image, ImageDraw
import os
import numpy as np
import matplotlib.pyplot as plt


# Функция для вычисления среднего цвета
def average_color(image):
    np_image = np.array(image)
    w, h, d = np_image.shape
    return tuple(np_image.reshape(w * h, d).mean(axis=0).astype(int))


def get_average_colors(img):
    width, height = img.size
    # Разделяем изображение на 4 части
    parts = [
        img.crop((0, 0, width // 2, height // 2)),  # Верхний левый
        img.crop((width // 2, 0, width, height // 2)),  # Верхний правый
        img.crop((0, height // 2, width // 2, height)),  # Нижний левый
        img.crop((width // 2, height // 2, width, height))  # Нижний правый
    ]

    average_colors = [average_color(part) for part in parts]

    return average_colors


def fill_img_average_colors(draw, img, average_colors):
    width, height = img.size
    draw.rectangle([(0, 0), (width // 2, height // 2)], fill=average_colors[0])  # Верхний левый
    draw.rectangle([(width // 2, 0), (width, height // 2)], fill=average_colors[1])  # Верхний правый
    draw.rectangle([(0, height // 2), (width // 2, height)], fill=average_colors[2])  # Нижний левый
    draw.rectangle([(width // 2, height // 2), (width, height)], fill=average_colors[3])  # Нижний правый


# Для демонстрации работы
def display_images_with_average_colors(image_path):
    """
    Выводит на экран исходное изображение и рядом усреднённое

    :param image_path: Path to the input image.
    """
    with Image.open(image_path) as img:
        average_colors = get_average_colors(img)

    # Отображаем оригинальное изображение
    original_img = Image.open(image_path)
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(original_img)
    plt.title("Оригинальное изображение")
    plt.axis('off')

    width, height = img.size
    new_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(new_image)

    draw.rectangle([(0, 0), (width // 2, height // 2)], fill=average_colors[0])  # Верхний левый
    draw.rectangle([(width // 2, 0), (width, height // 2)], fill=average_colors[1])  # Верхний правый
    draw.rectangle([(0, height // 2), (width // 2, height)], fill=average_colors[2])  # Нижний левый
    draw.rectangle([(width // 2, height // 2), (width, height)], fill=average_colors[3])  # Нижний правый

    # Отображаем среднего изображения
    plt.subplot(1, 2, 2)
    plt.imshow(new_image)
    plt.title("Новое изображение")
    plt.axis('off')

    plt.tight_layout()
    plt.show()


class Img:
    def __init__(self, name):
        self.name = name
        with Image.open(name) as img:
            self.img = img.copy()
        self.used_count = 0
        self.average_color_parts = get_average_colors(self.img)

    def compare(self, average_colors):
        res = 0
        for i in range(len(average_colors)):
            res += abs(average_colors[i][0] - self.average_color_parts[i][0])
            res += abs(average_colors[i][1] - self.average_color_parts[i][1])
            res += abs(average_colors[i][2] - self.average_color_parts[i][2])
        res += self.used_count * 2
        return res


if __name__ == "__main__":
    image_path = 'images/sources/1l6Te7eTguk.jpg'
    display_images_with_average_colors(image_path)

