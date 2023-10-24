import argparse
import requests

from django.core.exceptions import MultipleObjectsReturned
from os.path import splitext, split
from urllib.parse import urlsplit, unquote

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import PlaceName, PlaceImage
from where_to_go_v2 import settings


base_path = settings.BASE_DIR


def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def upload_data_to_db(url):
    """Загружаем данные в БД"""
    response = requests.get(url)
    response.raise_for_status()
    place_raw = response.json()

    imgs = place_raw["imgs"]
    title = place_raw["title"]
    try:
        location, created = PlaceName.objects.update_or_create(
            title=title,
            short_description=place_raw["description_short"],
            long_description=place_raw["description_long"],
            latitude=place_raw["coordinates"]["lat"],
            longitude=place_raw["coordinates"]["lng"]
        )
    except MultipleObjectsReturned:
        return print("Ошибка: Существует несколько объектов с таким заголовком.")

    for img_url in imgs:
        img_name, img_extension = get_filename_and_ext(img_url)
        img_upload = PlaceImage.objects.create(place=location)
        img_response = requests.get(img_url, stream=True)
        img_response.raise_for_status()
        img_upload.picture.save(f"{img_name}.{img_extension}", ContentFile(img_response.content))

    return f"Данные для места '{title}' успешно загружены. Загружено {len(imgs)} изображений."


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
