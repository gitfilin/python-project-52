from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Hello, Hexlet! Welcome to task_manager.</h1>')
