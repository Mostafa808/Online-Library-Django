from django.core.handlers import wsgi
from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader
# Create your views here.
def home(request: wsgi.WSGIRequest):
    page = loader.get_template("Home.html")
    return HttpResponse(page.render())

def books(request: wsgi.WSGIRequest):
    page = loader.get_template("Books.html")
    return HttpResponse(page.render())
def account_sign_in(request: wsgi.WSGIRequest):
    page = loader.get_template("Sign-Up.html")
    return HttpResponse(page.render())
def account_sign_up(request: wsgi.WSGIRequest):
    page = loader.get_template("Sign-In.html")
    return HttpResponse(page.render())