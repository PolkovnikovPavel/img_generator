from PIL import Image
import os
from canvas import *


def get_sizes(xn, yn, start_size):
    """
    :param xn: дробление по x
    :param yn: дробление по y
    :param start_size: (width, height) исходного изображения
    :return: возвращает новые размеры изображения и размеры для всех фрагментов
    """
    x = start_size[0] // xn
    y = start_size[1] // yn
    new_size = (x * xn, y * yn)
    return new_size, (x, y)


def process_sources_img(size):
    """
    Из папки sources переводит все изображения к новому формату в папку processed.
    :param size: размер фрагментов (width, height)
    :return:
    """
    input_folder = 'images/sources'
    output_folder = 'images/processed'
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                resized_img = img.resize(size)
                output_path = os.path.join(output_folder, filename)
                resized_img.save(output_path)


if __name__ == "__main__":
    name = 'images/main.jpg'
    name_to_save = 'images/main2.jpg'

    with Image.open(name) as img:
        width, height = img.size
        new_size, size_fragments = get_sizes(50, 50, (width, height))
        base_img = img.resize(new_size)

    print(f'Обработка изображений к размеру {size_fragments}...')
    # process_sources_img(size_fragments)

    canvas = Canvas(None, base_img=base_img)

    print('Загрузка изображений...')
    canvas.load_all_imgs('images/processed')

    print('Создание фрагментов...')
    canvas.create_fragments()

    print('Выбор подходящих картинок', end='')
    canvas.set_ratings()

    print('\nФинальная обработка...')
    canvas.create_result()

    print()
    print(f'Результат сохранён как {name_to_save}')
    canvas.new_img.save('images/main2.jpg')



