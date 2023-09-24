from django.shortcuts import render
import json
from places.models import PlaceName


def serialize_post(post):
    data = {
        'title': post.title,
        'imgs': [pic.picture.url for pic in post.pictures.all().order_by('numb')],
        'short_description': post.short_description,
        'long_description': post.long_description,
        'coordinates': {
            'longitude': post.longitude,
            'latitude': post.latitude,
        }
    }
    with open(f"static/places/{post.slug}.json", "w") as outfile:
        json.dump(data, outfile)

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [post.point_lon, post.point_lat]
        },
        "properties": {
            "title": post.title.split("«")[1],
            "placeId": post.slug,
            "detailsUrl": f'static/json/{post.slug}.json'
        }
    }


def index(request):
    posts = PlaceName.objects.all()
    context = {
        'places_posts': {"type": "FeatureCollection",
                         "features": [
                             serialize_post(post) for post in posts
                         ]}
    }
    return render(request, 'places/index.html', context)
