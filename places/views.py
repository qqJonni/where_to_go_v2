from django.shortcuts import render, get_object_or_404
from places.models import PlaceName
from django.urls import reverse
from django.http import HttpResponse, JsonResponse


def serialize_post(post):
    redirect_url = reverse('details_json', args=[post.pk])

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [post.longitude, post.latitude]
        },
        "properties": {
            "title": post.title,
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


def details_json(request, pk):
    post = get_object_or_404(PlaceName, pk=pk)
    post_data = {
        "title": post.title,
        "imgs": [
            pic.picture.url for pic in post.pictures.all().order_by('numb')
        ],
        "description_short": post.short_description,
        "description_long": post.long_description,
        "coordinates": {
            "lng": post.longitude,
            "lat": post.latitude
        }
    }
    output = JsonResponse(post_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
    return HttpResponse(output, content_type="application/json")
