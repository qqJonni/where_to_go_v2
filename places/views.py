from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import PlaceName


def serialize_post(location):
    redirect_url = reverse('get_details_json', args=[location.pk])

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [location.longitude, location.latitude]
        },
        "properties": {
            "title": location.title,
            "detailsUrl": redirect_url
        }
    }


def index(request):
    locations = PlaceName.objects.all()
    context = {
        'places_posts': {"type": "FeatureCollection",
                         "features": [
                             serialize_post(location) for location in locations
                         ]}
    }
    return render(request, 'places/index.html', context)


def get_details_json(request, pk):
    location = get_object_or_404(PlaceName.objects.prefetch_related('pictures'), pk=pk)

    location_information = {
        "title": location.title,
        "imgs": [pic.picture.url for pic in location.pictures.order_by('sequence_number')],
        "description_short": location.short_description,
        "description_long": location.long_description,
        "coordinates": {
            "lng": location.longitude,
            "lat": location.latitude
        }
    }

    return JsonResponse(location_information, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
