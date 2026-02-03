from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    """Главная страница"""
    return render(request, 'lib_app/index.html')


def about(request):
    """Страница о нас"""
    return HttpResponse('<h1>О нас!</h1>')
