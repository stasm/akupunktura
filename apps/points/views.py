from django.http import HttpResponse
from django.shortcuts import render_to_response

from points.models import Point

def home(request):
    points = Point.objects.recently_added()
    return render_to_response('points/home.html',
                              {'points': points})
