import os
import argparse
from dotenv import load_dotenv

from image_downloader import download_image


from datetime import datetime
import requests


def build_epic_image_links(api_key):
    if not api_key:
        raise ValueError('NASA API ключ не задан.')

    epic_api_endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    request_params = {'api_key': api_key}

    response = requests.get(epic_api_endpoint, params=request_params)
    response.raise_for_status()

    image_metadata_list = response.json()
    image_links = []

    for image_metadata in image_metadata_list:
        photo_captured_at = datetime.strptime(image_metadata['date'], '%Y-%m-%d %H:%M:%S')
        epic_filename = image_metadata['image']

        epic_link = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{photo_captured_at:%Y/%m/%d}/png/{epic_filename}.png'
            f'?api_key={api_key}'
        )

        image_links.append((epic_link, epic_filename))

    return image_links


def fetch_epic_images(api_key, max_images=10):
    epic_links_with_filenames = build_epic_image_links(api_key)[:max_images]

    for index, (epic_link, original_filename) in enumerate(epic_links_with_filenames, start=1):
        result_filename = f'epic{index}.png'
        final_filepath = os.path.join('space_gallery', result_filename)
        download_image(epic_link, final_filepath)


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

    fetch_epic_images(args.api_key, max_images=args.count)


if __name__ == '__main__':
    main()