from django.shortcuts import render
from django.http import HttpResponse

def calculate():
    x = 10
    y = 20 
    return x + y

def say_hello(request):
   x = calculate()
   return render(request, "hello.html", {"name": "Django"})