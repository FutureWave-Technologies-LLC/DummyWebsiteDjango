from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

# View function for home page
def home(request):
    return render(request, 'home.html')

# View function for login page
def login_page(request):
    # Check if HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user with the provided username exists
        if not User.objects.filter(username=username).exists():

            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to home page upon sign in
            return redirect('/home/')

# View function for registration page
def register_page(request):
    # Check if HTTP request method is POST (form submission)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
    # Check if user with provided username already exists
    user = User.objects.filter(username=username)

    if user.exists():
        # Display information message if username is taken
        messages.info(request, "Username is already taken")
        return redirect('/register/')

    # Create a new User object with the provided information
    user = user.objects.create_user(
        username=username,
    )

    # Set user's password and save user object
    user.set_password(password)
    user.save()

    # Display information message indicating successful acount creation
    messages.info(request, "Account created Successfully")
    return redirect('/register/')

    # Render the registration page template (GET request)
    return render(request, 'register.html')

@api_view(['GET'])
def get_messages(request):
    data = messages.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_replies(request):
    data = replies.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_comments(request):
    data = comments.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_posts(request):
    data = posts.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_personal_pages(request):
    data = personal_pages.objects.all().values()
    return Response(list(data))

@api_view(['GET', 'POST'])
def get_users(request):
    if request.method == 'POST':
        data = request.data

        my_user = users.objects.all().filter(user_id = 0).first()  
        
        # my_user = users.objects.create(user_id = '10').last()
        my_user.username = data.get('username')
        my_user.password = data.get('password')
        my_user.status = True
        my_user.save()
        json_data = serializers.serialize('json', [my_user])

        # Return the JSON response
        return JsonResponse(json_data, safe=False)
        #from the previous user check the likes_count
    elif request.method == 'GET':
        data = users.objects.all().values()
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
@api_view(['POST'])
def update_username(request):
    my_user = users.objects.all().filter(username = "John").first()
    #my_user.username == input from user goes here
    my_user.save()
    json_data = serializers.serialize('json', [my_user])
    # Return the JSON response
    return JsonResponse(json_data, safe=False)
    #from the previous user check the likes_count

#def home(request):
        #return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")
