import os
import requests
from datetime import datetime
from urllib.parse import urlsplit, unquote
from dotenv import load_dotenv


load_dotenv()
nasa_token = os.getenv('NASA_API_KEY')


def download_image(image_link, target_filepath):
    os.makedirs(os.path.dirname(target_filepath), exist_ok=True)

    response = requests.get(image_link)
    response.raise_for_status()

    with open(target_filepath, 'wb') as file:
        file.write(response.content)


def extract_file_extension(image_link):
    image_path = urlsplit(image_link).path
    image_filename = os.path.basename(unquote(image_path))
    _, extension = os.path.splitext(image_filename)
    return extension


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


if __name__ == '__main__':
    if not nasa_token:
        raise RuntimeError('NASA_API_KEY не найден в .env')

    fetch_epic_images(nasa_token, max_images=5)