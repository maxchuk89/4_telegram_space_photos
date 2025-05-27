import os
import argparse
from datetime import datetime
import requests
from dotenv import load_dotenv

from image_downloader import download_image


def get_epic_image_links(api_key, max_images):
    epic_api_endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    request_params = {'api_key': api_key}
    response = requests.get(epic_api_endpoint, params=request_params)
    response.raise_for_status()

    image_metadata_list = response.json()
    image_links = []

    for image_metadata in image_metadata_list[:max_images]:
        photo_captured_at = datetime.strptime(image_metadata['date'], '%Y-%m-%d %H:%M:%S')
        epic_filename = image_metadata['image']
        epic_link = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{photo_captured_at:%Y/%m/%d}/png/{epic_filename}.png'
            f'?api_key={api_key}'
        )
        image_links.append((epic_link, epic_filename))

    return image_links


def download_epic_images(image_links_with_names):
    for index, (epic_link, _) in enumerate(image_links_with_names, start=1):
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

    image_links = get_epic_image_links(args.api_key, args.count)
    download_epic_images(image_links)


if __name__ == '__main__':
    main()