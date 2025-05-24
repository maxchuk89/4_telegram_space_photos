import os
import argparse
import requests

from image_downloader import download_image


def fetch_spacex_images(launch_identifier=None):
    if not launch_identifier:
        launch_identifier = '5eb87d47ffd86e000604b38a'

    spacex_api_url = f'https://api.spacexdata.com/v5/launches/{launch_identifier}'

    response = requests.get(spacex_api_url)
    response.raise_for_status()

    launch_metadata = response.json()
    photo_links = launch_metadata['links']['flickr']['original']

    for index, photo_link in enumerate(photo_links, start=1):
        filename = f'spacex{index}.jpg'
        target_filepath = os.path.join('space_gallery', filename)
        download_image(photo_link, target_filepath)


def main():
    parser = argparse.ArgumentParser(
        description='Скачивает изображения запуска SpaceX по ID или фиксированному запуску'
    )
    parser.add_argument('--launch-id', help='ID запуска (по умолчанию: 5eb87d47ffd86e000604b38a)')
    args = parser.parse_args()

    fetch_spacex_images(args.launch_id)


if __name__ == '__main__':
    main()