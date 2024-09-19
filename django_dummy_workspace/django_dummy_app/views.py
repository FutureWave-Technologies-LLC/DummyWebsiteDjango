from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import client_info
from .models import likes
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

@api_view(['GET'])
def get_client_info(request):
    data = client_info.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_likes(request):
    data = likes.objects.all().values()
    return Response(list(data))

@api_view(['POST'])
def update_likes(request):
    my_user = likes.objects.filter(email = "email@gmial.com").first()
    my_user.like_count += 1 #update like count for this user to be like_count + 1
    my_user.save()
    json_data = serializers.serialize('json', [my_user])

    # Return the JSON response
    return JsonResponse(json_data, safe=False)
    #from the previous user check the likes_count

def home(request):
        return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")
# Create your views here.
