from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    """Главная страница"""
    return HttpResponse('<h1>Привет всем!</h1>')


def about(request):
    """Страница о нас"""
    return HttpResponse('<h1>О нас!</h1>')
