from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse

# Create your views here.

@api_view(['GET'])
def get_users(request):
    data = users.objects.all().values()
    return Response(list(data))
def get_personal_pages(request):
    data = personal_pages.objects.all().values()
    return Response(list(data))
def get_posts(request):
    data = posts.objects.all().values()
    return Response(list(data))
def get_comments(request):
    data = comments.objects.all().values()
    return Response(list(data))
def get_replies(request):
    data = replies.objects.all().values()
    return Response(list(data))
def get_messages(request):
    data = messages.objects.all().values()
    return Response(list(data))

def home(request):
        return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")