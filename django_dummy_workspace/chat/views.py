from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatmessageCreateForm

# Create your views here.

# From this tutorial https://youtu.be/Q7N2oJTnThA?si=Nbhy02sBxpZk-g3r. 
# This will have to be changed to connect to React. 

#@login_required    # The tutorial uses this decorator, but I don't know if it's compatible with our models
def message_view(request):
    chat = get_object_or_404(ChatGroup, chat_name="chat")   # Double check if names align w/models
    chat_messages = chat.chat_messages.all()[:30]                 # Double check if names align w/models
    form = ChatmessageCreateForm()

    if request.method == 'POST':    # This was the last step of the tutorial I followed, from here it goes into htmx, hyperscript, and CSS animation
        form = ChatmessageCreateForm(request.Post)
        if form.is_valid:
            message = formsave(commit=False)
            message.author = request.users
            message.group = chat_group
            message.save()
            return redirect('messages/')

    return render(request, 'messages/chat.html', {'chat_messages' : chat_messages}) # Double check if names align w/models