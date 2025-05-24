import os
import argparse
import requests
from dotenv import load_dotenv

from image_downloader import download_image, extract_file_extension


def fetch_apod_images(api_key, image_count):
    if not api_key:
        raise RuntimeError('NASA API ключ не указан и не найден в .env')

    nasa_apod_api = 'https://api.nasa.gov/planetary/apod'
    request_params = {'count': image_count, 'api_key': api_key}

    response = requests.get(nasa_apod_api, params=request_params)
    response.raise_for_status()

    image_metadata_list = response.json()

    for index, image_metadata in enumerate(image_metadata_list, start=1):
        if image_metadata.get('media_type') != 'image':
            continue

        image_link = image_metadata['url']
        extension = extract_file_extension(image_link)
        filename = f'nasa{index}{extension}'
        target_filepath = os.path.join('space_gallery', filename)

        download_image(image_link, target_filepath)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает изображения с NASA APOD (Astronomy Picture of the Day)'
    )
    parser.add_argument('--api-key', default=os.getenv('NASA_API_KEY'), help='API-ключ NASA')
    parser.add_argument('--count', type=int, default=5, help='Количество изображений (по умолчанию 5)')
    args = parser.parse_args()

    fetch_apod_images(args.api_key, args.count)


if __name__ == '__main__':
    main()
