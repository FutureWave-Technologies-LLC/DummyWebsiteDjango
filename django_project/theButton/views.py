from django.shortcuts import render
from rest_framework import generics
from .models import dummydata
from rest_framework.response import Response
from .serializer import dummydataserializer

# Create your views here.

class getdummydata(generics.ListAPIView):
    queryset = dummydata.objects.all()
    serializer_class = dummydataserializer