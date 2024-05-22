from django.core.handlers import wsgi
from django.shortcuts import render
from .models import User, BookDetails, BookCopy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
import json

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

@csrf_exempt
def account_sign_in_action(request: wsgi.WSGIRequest):
    if request.method=="POST":
        response_message = {"valid":True, "message":"You have signed in successfully!", "user": {}}
        current_token = dict(json.loads(request.body))
        print("Try signing in with: ", current_token)
        current_user = User.objects.get(username = current_token["username"])
        if current_user:
            if current_user.password==current_token["password"]:
                response_message["user"] = model_to_dict(current_user)
                print("Signed In with: ", current_user)
            else:
                response_message = {"valid":False, "message":"Username or Password is incorrect", "user": {}}
            
        else:
            response_message = {"valid":False, "message":"Username or Password is incorrect", "user": {}}
        return(JsonResponse(response_message))
    else:
        return(JsonResponse({"error":"invalid request"}))
    
@csrf_exempt
def account_sign_up_action(request: wsgi.WSGIRequest):
    if request.method=="POST":
        current_user = dict(json.loads(request.body))["user"]
        print(current_user,end="\n\n")
        result = User.pre_add_validation(current_user)
        if(result["valid"]):
            try:
                current_user["website_view"] = User.view_code(current_user["website_view"])
                if current_user["website_view"]==-1:
                    result = {"valid":False, "message":"The user view is not recognized."}
                else:
                    current_user_model = User(username=current_user["username"], password=current_user["password"], full_name=current_user["full_name"], email=current_user["email"], address=current_user["address"], birth_date=current_user["birth_date"], is_admin=current_user["is_admin"], profile_image_link=current_user["profile_image_link"], website_view=current_user["website_view"])
                    print("Added: ", current_user_model)
                    current_user_model.save()
                    result = {"valid":True, "message":"You have signed up successfully!"}
            except Exception as error:
                print(error)
                result = {"valid":False, "message":"Failed to add the new user to the database"}
        return(JsonResponse(result))
    else:
        return(JsonResponse({"error":"invalid request"}))
