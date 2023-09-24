from django.shortcuts import render
from places.models import PlaceName
from django.urls import reverse


def serialize_post(post):
    redirect_url = reverse('details_json', args=[post.pk])

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [post.longitude, post.latitude]
        },
        "properties": {
            "title": post.title.split("«")[1],
            "placeId": post.slug,
            "detailsUrl": redirect_url
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
