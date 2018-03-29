from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# API Message CURD

def index(request):
    return HttpResponse("Hello, world. You're at the msg index.")
