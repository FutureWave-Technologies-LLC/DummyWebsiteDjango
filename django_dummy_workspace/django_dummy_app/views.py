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
from random import randrange

# Create your views here.

# View function for home page
def home(request):
    return render(request, 'home.html')

@api_view(['GET', 'POST'])
def get_users(request):
    if request.method == 'POST':
        data = request.data 
        user = users.objects.filter(username=data.get('username')).first()
        if user:
            # Display information message if username is taken
            json_data = {"response": "Username already exists, please choose another username", "error": True}
            # Return the JSON response
            return JsonResponse(json_data, safe=False)
        if len(data.get('password')) < 4:
            # Display information message if username is taken
            json_data = {"response": "Password must be more than 4 characters long", "error": True}
            # Return the JSON response
            return JsonResponse(json_data, safe=False)
        my_user = users.objects.all().count()
        my_user_info = users(user_id = my_user, username = data.get('username'), password = data.get('password')
                             ,status = False, first_name = data.get('first_name'), last_name = data.get('last_name'))
        my_user_info.save()
        json_data = {"response": "User was created", "error": False}
        # Return the JSON response
        return JsonResponse(json_data, safe=False)
        #from the previous user check the likes_count
    elif request.method == 'GET':
        data = users.objects.all().values()
        return Response(list(data))
    
#Gets a user's data based on username
@api_view(['GET'])
def get_user_data(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()
    
    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        data = user.values()
        return(Response(data))
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    
#Update token for a user
@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()
    
    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        print("password match")
        #data to be stored to token by frontend
        json_data = {"username": user.username,
                     "token_id": randrange(1, 100000, 1)
                     }
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)

    
@api_view(['POST'])
def recieving_posts(request):
    data = request.data
    my_post_id = posts.objects.all().count()
    my_post_info = posts(post_id = my_post_id, media = 'media', text = data.get('postText'), user_id = '9', title = data.get('title'), username = 'usernameGoesHere')
    my_post_info.save()
    json_data = {"Response": "Post was created", "error": False}
    return JsonResponse(json_data, safe=False)

@api_view(['GET'])
def get_post_data(request):
    data = posts.objects.all().values()
    return(Response(data))

# View function for login page
@api_view(['POST'])
def login_page(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    print("test")
    #fetching the user from database
    user = users.objects.filter(username=username).first()
    if not user:
        # Display an error message if the username does not exist
        json_data = {"response": "Username was not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    # Check if user with the provided username exists
    #if password doesn't match return error
    #TBD: Function that compares password hashes
    if user.password != password:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    # Log in the user and redirect to home page upon sign in
    json_data = {"response": "Valid user", "error": False}
    return JsonResponse(json_data, safe=False)

# View function for registration page
@api_view(['POST'])
def register_page(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    # Check if user with provided username already exists
    user = users.objects.filter(username=username)

    if user.exists():
        # Display information message if username is taken
        messages.info(request, "Username is already taken")
        return redirect('/register/')

    # Create a new User object with the provided information
    user = users.objects.create_user(
        username=username,
    )

    # Set user's password and save user object
    user.set_password(password)
    user.save()

    # Display information message indicating successful acount creation
    messages.info(request, "Account created Successfully")
    return redirect('/register/')

@api_view(['GET'])
def get_messages_for_chat(request, chat_id):
        # Filter messages by chat_id passed in the URL
        messages_in_chat = messages.objects.filter(chat_id=chat_id)

        # If no messages are found for the chat
        if not messages_in_chat.exists():
            json_data = {"response": "No messages found for this chat", "error": True}
            return JsonResponse(json_data, safe=False)

        # Serialize the messages
        serializer = MessageSerializer(messages_in_chat, many=True)

        # Return the serialized messages in the desired JSON format
        json_data = {
            "response": serializer.data,
            "error": False
        }
        return JsonResponse(json_data, safe=False)

@api_view(['POST'])
def send_message(request):
    # Deserialize the incoming message data
    serializer = MessageSerializer(data=request.data)
    
    # If the data is valid, save the new message
    if serializer.is_valid():
        serializer.save(sender=request.user)  # Assuming the sender is the logged-in user

        # Return a success response with the created message data
        json_data = {
            "response": serializer.data,
            "error": False
        }
        return JsonResponse(json_data, safe=False, status=201)

    # If the data is invalid, return an error response
    json_data = {
        "response": serializer.errors,
        "error": True
    }
    return JsonResponse(json_data, safe=False, status=400)

@api_view(['POST'])
def get_chat_info(request):
    user1_id = request.data.get('user1_id')
    user2_id = request.data.get('user2_id')

    # Find chat where both users are participants
    chats_user1 = chat_participants.objects.filter(user_id=user1_id).values_list('chat_id', flat=True)
    chats_user2 = chat_participants.objects.filter(user_id=user2_id).values_list('chat_id', flat=True)

    # Find the common chat
    common_chat = set(chats_user1).intersection(set(chats_user2))
    if common_chat:
        chat_id = list(common_chat)[0]  # Assuming only one chat is found between the users
        chat = Chat.objects.get(id=chat_id)
        return JsonResponse({"chat_id": chat.id, "created_at": chat.created_at}, status=200)
    else:
        return JsonResponse({"error": "No common chat found"}, status=404)
    
@api_view(['POST'])
def create_chat(request):
    user1_id = request.data.get('user1_id')
    user2_id = request.data.get('user2_id')

    # Create a new chat
    chat = Chat.objects.all().count()
    my_chat = Chat(id = chat)  # adding one to the number of Chat ids
    my_chat.save()

    # Add both users to the chat_participants table
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    chat_participants.objects.create(chat=chat, user=user1)
    chat_participants.objects.create(chat=chat, user=user2)

    return JsonResponse({"chat_id": chat.id, "created_at": chat.created_at}, status=201)

#Gets a user's data based on username
@api_view(['GET'])
def get_user_data(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()

    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        data = user.values()
        return(Response(data))
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)

#Update token for a user
@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()

    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        print("password match")
        #data to be stored to token by frontend
        json_data = {"username": user.username,
                     "token_id": randrange(1, 100000, 1)
                     }
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)

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

#def home(request):
        #return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")
