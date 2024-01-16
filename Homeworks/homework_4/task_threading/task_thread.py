# Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# Программа должна использовать многопоточный подход.
# Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.
import sys

import requests
import os
import threading
import time
import argparse
from urllib.parse import urlparse


# через os.path
def download_image(url, foldername):
    start_time = time.time()  # Move start_time inside the function

    try:
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists(foldername):
                os.makedirs(foldername)

            filename = os.path.join(foldername, os.path.basename(url))
            with open(filename, 'wb') as file:
                file.write(response.content)
            end_time = time.time()
            result_time = end_time - start_time

            print(f"Изображение {url} загружено по пути: {filename} за {result_time:.2f} секунд")
        else:
            print(f"Сбой загрузки изображения {url}")
    except Exception as e:
        print(f"Сбой загрузки изображения {url}: {e}")


# можно было через url.parse
# def download_image(url, foldername):
#     try:
#         parsed_url = urlparse(url)
#         if parsed_url.scheme and parsed_url.netloc:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 if not os.path.exists(foldername):
#                     os.makedirs(foldername)
#
#                 filename = os.path.join(foldername, os.path.basename(parsed_url.path))
#                 with open(filename, 'wb') as file:
#                     file.write(response.content)
#                 print(f"Изображение {url} загружено по пути: {filename}")
#             else:
#                 print(f"Сбой загрузки изображения {url}")
#         else:
#             print(f"Invalid URL: {url}")
#     except Exception as e:
#         print(f"Сбой загрузки изображения {url}: {e}")


# этот метод запускается из командной строки с передачей урлов через пробел
def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', metavar='URL', type=str, nargs='+')
    args = parser.parse_args()
    foldername = "downloads_command_line"
    start_time = time.time()
    threads = []
    for url in args.urls:
        thread = threading.Thread(target=download_image, args=(url, foldername))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Затраченное время: {end_time - start_time:.2f} секунд")


# запуск метода кнопкой с передачей списка урлов, либо в командной строке без передачи аргументов
def run_button(urls):
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', metavar='URL', type=str, nargs='+')
    foldername = "downloads_run_button"
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url, foldername))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Затраченное время: {end_time - start_time:.2f} секунд")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Для запуска в терминале:
        # у меня убунту, поэтому моя команда выглядит так:
        # (интерпретатор скрипт.py урл_адресы_изображения_через_пробел)
        # python3 task_thread.py https://24warez.ru/uploads/posts/2013-09/1378297750_5.jpg https://dasart.ru/userdata/image/dd/e2/dde26818ca61428f7e2c65bfceb69a54.jpg

        print("Вызов метода command_line():")
        command_line()
    else:
        # Для запуска кнопкой в Pycharm либо в терминале без передачи аргументов
        # Достаточно в Pycharm нажать на треугольник:
        # список урлов прилагается
        urls = [
            'https://fireseo.ru/wp-content/uploads/2020/04/besplatnye-kartinki.jpg',
            'https://24warez.ru/uploads/posts/2013-09/1378297780_1.jpg',
            'https://dasart.ru/userdata/image/45/42/45421a14ec6c8ff137c09cb3281c70a7.jpg'
        ]

        # вызов метода для запуска с кнопки
        print("Вызов метода run_button(urls):")
        run_button(urls)
