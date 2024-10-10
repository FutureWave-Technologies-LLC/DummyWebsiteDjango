# From this tutorial https://youtu.be/Q7N2oJTnThA?si=Nbhy02sBxpZk-g3r.
# This is my first time hearing about forms, but here's the documentation for it: https://docs.djangoproject.com/en/5.0/topics/forms/

from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlength' : '300', 'autofocus': True }),
        }

class NewGroupForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['chat_name']
        widgets = {
            'chat_name' : forms.TextInput(attrs={
                'placeholder': 'Add name ...', 
                'class': 'p-4 text-black', 
                'maxlength' : '300', 
                'autofocus': True,
                }),
        }
        
        
class ChatRoomEditForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['chat_name']
        widgets = {
            'chat_name' : forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4', 
                'maxlength' : '300', 
                }),
        }