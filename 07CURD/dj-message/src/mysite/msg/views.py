from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Message
# API Message CURD

class IndexView(generic.ListView):
    def get_queryset(self):
        """Return the last five published questions."""
        return Message.objects.order_by('-createAt')[:5]

