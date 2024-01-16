# Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# Программа должна использовать асинхронный подход.
# Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.

import aiohttp
import aiofiles
from asyncio import gather, run
import os
import time
import argparse
import sys


# async def download_image(url, foldername):
#     start_time = time.time()
#     filename = os.path.join(foldername, os.path.basename(url))
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 if not os.path.exists(foldername):
#                     os.makedirs(foldername)
#
#                 with open(filename, 'wb') as file:
#                     while True:
#                         chunk = await response.content.read(1024)
#                         if not chunk:
#                             break
#                         file.write(chunk)
#                 end_time = time.time()
#                 print(f"Изображение {url} загружено по пути: {filename} за {end_time - start_time:.2f} секунд")
#             else:
#                 print(f"Сбой загрузки изображения {url}")
async def download_image(url, foldername):
    start_time = time.time()
    filename = os.path.join(foldername, os.path.basename(url))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                if not os.path.exists(foldername):
                    os.makedirs(foldername)
                # чанки позволяют эффективно обрабатывать большие файлы
                # асинхроный метод aiofiles.open позволяет выполнять запись файла асинхронно с http запросом
                async with aiofiles.open(filename, 'wb') as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        await file.write(chunk)
                end_time = time.time()
                print(f"Изображение {url} загружено по пути: {filename} за {end_time - start_time:.2f} секунд")
            else:
                print(f"Сбой загрузки изображения {url}")


# этот метод запускается из командной строки
async def run_async(urls, foldername):
    start_time = time.time()
    tasks = [download_image(url, foldername) for url in urls]
    await gather(*tasks)
    end_time = time.time()
    print(f"Затраченное время: {end_time - start_time:.2f} секунд")


# этот метод просто меняет папку чтобы понимать, что было запущено кнопкой, либо запуск в командной строке
# без передачи аргументов тогда он возьмет аргументы, записанные в urls...
async def run_asyncio(urls):
    foldername = "downloads_run_button"
    await run_async(urls, foldername)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Для запуска в терминале:
        # у меня убунту, поэтому моя команда выглядит так:
        # (интерпретатор скрипт.py урл_адресы_изображения_через_пробел)
        # python3 task_async.py https://24warez.ru/uploads/posts/2013-09/1378297750_5.jpg https://dasart.ru/userdata/image/dd/e2/dde26818ca61428f7e2c65bfceb69a54.jpg

        print("Вызов метода run_async() в командной строке:")
        run(run_async(sys.argv[1:], "downloads_command_line"))
    else:
        # Для запуска кнопкой в Pycharm либо в терминале без передачи аргументов
        # Достаточно в Pycharm нажать на треугольник:
        # список урлов прилагается
        urls = [
            'https://fireseo.ru/wp-content/uploads/2020/04/besplatnye-kartinki.jpg',
            'https://24warez.ru/uploads/posts/2013-09/1378297780_1.jpg',
            'https://dasart.ru/userdata/image/45/42/45421a14ec6c8ff137c09cb3281c70a7.jpg'
        ]
        print("Вызов метода run_asyncio(urls):")
        run(run_asyncio(urls))
