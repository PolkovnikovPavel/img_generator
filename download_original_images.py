import vk_api
import requests
import datetime
import cv2 as cv
import numpy as np
import os

from auth import *   # данные аутентификации


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def two_factor():
    code = input('Code? ')
    return code, 1


def save_img(url, path):
    p = requests.get(url)
    out = open(path, "wb")
    out.write(p.content)
    out.close()


def main():
    vk_session = vk_api.VkApi(login, password, auth_handler=two_factor, captcha_handler=captcha_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    all_names = []
    count = 0
    offset = 0
    is_out = False

    while True:
        try:
            response = vk.wall.get(count=100, domain='w_fredperry_w', offset=offset)
        except:
            continue
        if response['items']:
            for i in response['items']:
                if 'attachments' not in i:
                    continue
                for attachment in i['attachments']:
                    if attachment['type'] != 'photo':
                        continue
                    try:
                        url_photo = attachment['photo']['sizes'][4]['url']
                        name = url_photo.split('https://sun1-26.userapi.com')[-1].split('.jpg')[0].split('/')[-1]
                        if name not in all_names:
                            save_img(url_photo, f'{name_dir}/{name}.jpg')
                            count += 1
                            all_names.append(name)
                            print(count, url_photo)
                    except:
                        pass
                    if count == 96*54:
                        is_out = True
                        break
                if is_out:
                    break
                print()
        if is_out:
            break
        offset += 100


name_dir = 'imges_sciencemem'

if __name__ == '__main__':
    main()


