from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import client_info
from django.http import HttpResponse

@api_view(['GET'])
def get_dummy_data(request):
    data = client_info.objects.all().values()
    return Response(list(data))

def home(request):
        return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")
# Create your views here.
