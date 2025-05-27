import argparse
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from image_downloader import download_image


def get_epic_links(api_key, max_images):
    endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    params = {'api_key': api_key}
    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    items = response.json()
    links = []

    for item in items[:max_images]:
        date = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')
        name = item['image']
        link = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{date:%Y/%m/%d}/png/{name}.png'
            f'?api_key={api_key}'
        )
        links.append((link, name))

    return links


def download_epic_images(links):
    for index, (link, _) in enumerate(links, start=1):
        filename = f'epic{index}.png'
        filepath = os.path.join('space_gallery', filename)
        download_image(link, filepath)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает изображения Земли с NASA EPIC'
    )
    parser.add_argument('--api-key', default=os.getenv('NASA_API_KEY'), help='API-ключ NASA')
    parser.add_argument('--count', type=int, default=5, help='Количество изображений (по умолчанию 5)')
    args = parser.parse_args()

    if not args.api_key:
        raise RuntimeError('NASA_API_KEY не найден в .env и не передан через --api-key')

    links = get_epic_links(args.api_key, args.count)
    download_epic_images(links)


if __name__ == '__main__':
    main()