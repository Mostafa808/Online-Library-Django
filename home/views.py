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
    page = loader.get_template("Sign-In.html")
    return HttpResponse(page.render())
def account_sign_up(request: wsgi.WSGIRequest):
    page = loader.get_template("Sign-Up.html")
    return HttpResponse(page.render())
def profile(request: wsgi.WSGIRequest):
    page = loader.get_template("Profile.html")
    return HttpResponse(page.render())
def change_password (request: wsgi.WSGIRequest):
    page = loader.get_template("ChangePassword.html")
    return HttpResponse(page.render())
def books_admin(request: wsgi.WSGIRequest):
    page = loader.get_template("BooksAdmin.html")
    return HttpResponse(page.render())
def books_user(request: wsgi.WSGIRequest):
    page = loader.get_template("BooksUser.html")
    return HttpResponse(page.render())
def add_book(request: wsgi.WSGIRequest):
    page = loader.get_template("AddBook.html")
    return HttpResponse(page.render())

@csrf_exempt
def account_sign_in_action(request: wsgi.WSGIRequest):
    if request.method=="POST":
        response_message = {"valid":True, "message":"You have signed in successfully!", "user": {}}
        current_token = dict(json.loads(request.body))
        print("Try signing in with: ", current_token)
        current_user = User.objects.filter(username = current_token["username"])
        if current_user:
            current_user = User.objects.get(username = current_token["username"])
            if current_user.password==current_token["password"]:
                current_user.website_view = User.view_code_reverse(current_user.website_view)
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
        result = User.pre_add_validation(current_user)
        if(result["valid"]):
            try:
                current_user["website_view"] = User.view_code(current_user["website_view"])
                if current_user["website_view"]==-1:
                    result = {"valid":False, "message":"The user view is not recognized."}
                else:
                    current_user_model = User(username=current_user["username"], password=current_user["password"], full_name=current_user["full_name"], email=current_user["email"], address=current_user["address"], birth_date=current_user["birth_date"], is_admin=current_user["is_admin"], profile_image_link=current_user["profile_image_link"], website_view=current_user["website_view"])
                    current_user_model.save()
                    print("Added: ", current_user_model)
                    result = {"valid":True, "message":"You have signed up successfully!"}
            except Exception as error:
                print(error)
                result = {"valid":False, "message":"Failed to add the new user to the database"}
        return(JsonResponse(result))
    else:
        return(JsonResponse({"error":"invalid request"}))

@csrf_exempt
def account_update_action(request: wsgi.WSGIRequest):
    if request.method=="POST":
        current_user:dict = dict(json.loads(request.body))["user"]
        result = User.validate_permissions(current_user)
        if(not result["valid"]):
            return(JsonResponse(result))
        result = User.pre_add_validation(current_user, False)
        if(result["valid"]):
            try:
                current_user["website_view"] = User.view_code(current_user["website_view"])
                if current_user["website_view"]==-1:
                    result = {"valid":False, "message":"The user view is not recognized."}
                else:
                    current_user_model = User.objects.get(username=current_user["username"])
                    if "new_password" in current_user.keys():
                        current_user_model.password=current_user["new_password"]
                    else:
                        current_user_model.password=current_user["password"]
                    current_user_model.full_name=current_user["full_name"]
                    current_user_model.email=current_user["email"]
                    current_user_model.address=current_user["address"]
                    current_user_model.birth_date=current_user["birth_date"]
                    current_user_model.is_admin=current_user["is_admin"]
                    current_user_model.profile_image_link=current_user["profile_image_link"]
                    current_user_model.website_view=current_user["website_view"]                    
                    current_user_model.save()
                    print("Updated: ", current_user_model)
                    user_json = model_to_dict(current_user_model)
                    user_json["website_view"] = User.view_code_reverse(current_user_model.website_view)
                    result = {"valid":True, "message":"You have updated your profile successfully!", "user":user_json}
            except Exception as error:
                print(error)
                result = {"valid":False, "message":"Failed to update the user to the database"}
        return(JsonResponse(result))
    else:
        return(JsonResponse({"error":"invalid request"}))

@csrf_exempt
def books_add_book_action(request: wsgi.WSGIRequest):
    if request.method=="POST":
        current_user:dict = dict(json.loads(request.body))["user"]
        result = User.validate_permissions(current_user)
        if(not result["valid"]):
            return(JsonResponse(result))
        current_book_copy: dict = dict(json.loads(request.body))["current_book_copy"]
        current_book_details: dict = dict(json.loads(request.body))["current_book_details"]
        result = BookCopy.pre_add_validation(dict(json.loads(request.body))["current_book_copy"])
        if(result["valid"]):
            result = BookDetails.pre_add_validation(current_book_details)
            if(result["valid"]):
                if not result["reference"]:
                    new_details = BookDetails(
                        ISBN=current_book_details["ISBN"],
                        title=current_book_details["title"],
                        authors=current_book_details["authors"],
                        category=current_book_details["category"],
                        description=current_book_details["description"],
                        publisher=current_book_details["publisher"],
                        published_date=current_book_details["published_date"].split("T")[0]
                        )
                    new_details.save()
                ref_details = BookDetails.objects.get(ISBN=current_book_details["ISBN"])
                new_copy = BookCopy(
                    ID=current_book_copy["ID"],
                    details=ref_details,
                    printed_date=current_book_copy["printed_date"].split("T")[0]
                    )
                new_copy.save()
            
        return(JsonResponse(result))
    else:
        return(JsonResponse({"error":"invalid request"}))

@csrf_exempt
def books_search_action (request: wsgi.WSGIRequest):
    if request.method=="POST":
        print(request.body)
        current_user:dict = dict(json.loads(request.body))["user"]
        result = User.validate_permissions(current_user)
        if(not result["valid"]):
            return(JsonResponse(result))
        search_data = dict(json.loads(request.body))["search_data"]
        books_result = BookDetails.objects.filter(
            title__icontains=search_data["title"],
            category__icontains=search_data["category"],
            authors__icontains=search_data["author"]
            )
        
        list_details = [] 
        for key in books_result.values_list("ISBN"):
            list_details.append(key[0])
        print(list_details)
        copies_result = BookCopy.objects.filter(details__in=list_details)
        if search_data["is_available"]:
            copies_result = copies_result.filter(is_available=True)
        if search_data["is_borrowed"]:
            copies_result = copies_result.exclude(borrowed_by_id__isnull=True)
        
        context: dict = {
            "books": copies_result,
        }

        return(render(request, 'BooksResults.html', context))
    else:
        return(JsonResponse({"error":"invalid request"}))