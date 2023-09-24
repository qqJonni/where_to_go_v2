import argparse
from os.path import splitext, split
from pathlib import Path
from urllib.parse import urlsplit, unquote

from places.models import PlaceName, PlaceImage
from where_to_go_v2 import settings
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile


base_path = settings.BASE_DIR


def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def download_img(img_url, img_name, img_path):
    """Download the image"""
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'{img_path}/{img_name}', 'wb') as file:
        file.write(response.content)


def upload_data_to_db(url):
    """ Загружаем данные в БД """
    response = requests.get(url)
    response.raise_for_status()
    place_raw = response.json()
    imgs = place_raw["imgs"]
    img_names = []
    img_path = Path(base_path, 'static/imgs_data')
    img_path.mkdir(parents=True, exist_ok=True)
    for img_url in imgs:
        img_name, _ = get_filename_and_ext(img_url)
        img_names.append(img_name)
        download_img(img_url, img_name, img_path)
    location = PlaceName.objects.create(
        title=place_raw["title"],
        short_description=place_raw["description_short"],
        long_description=place_raw["description_long"],
        latitude=place_raw["coordinates"]["lat"],
        longitude=place_raw["coordinates"]["lng"]
    )
    for img in img_names:
        img_upload = PlaceImage.objects.create(place=location)
        with open(f'{img_path}/{img}', 'rb') as f:
            file = f.read()
            img_upload.picture.save(img, ContentFile(file), save=True)
    return 'OK'


class Command(BaseCommand):
    help = 'Загружаем данные в БД'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('url', nargs='+', type=str, help='Укажите Ссылку на json файл')
        url = parser.parse_args().url

        return url

    def handle(self, *args, **options):
        parser = argparse.ArgumentParser(
                    description="""
                    Программа загружает в БД по ссылке  на json файл
                    """, allow_abbrev=False)
        url = self.add_arguments(parser)[1]
        upload_data_to_db(url)
