from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.details_json, name='details_json')
]