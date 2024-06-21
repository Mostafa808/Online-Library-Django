from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class BookDetails(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True) 
    title = models.CharField(max_length=255)
    authors = models.JSONField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()

    def __str__(self):
        return self.title
    def pre_add_validation(book_details:dict):
        output = {"valid":True, "message":"The book copy and its details have been added.", "reference": False}
        if not book_details["ISBN"]:
            return {"valid":False, "message":"The book must have ISBN", "reference": False}
        if BookDetails.objects.filter(ISBN=book_details["ISBN"]):
            return {"valid":True, "message":"This ISBN already exists so the book copy have been added while referencing the old ISBN's details. If you want to change the old ISBN's details seek edit book page. Only copy ID, Print Date has been added.", "reference": True}
        if not book_details["title"]:
            return {"valid":False, "message":"The book must have title", "reference": False}
        authors: list = book_details["authors"]
        if not book_details["authors"][0]:
            return {"valid":False, "message":"The book must have authors", "reference": False}
        if not book_details["category"]:
            return {"valid":False, "message":"The book must have category", "reference": False}
        if not book_details["description"]:
            return {"valid":False, "message":"The book must have description", "reference": False}
        if not book_details["publisher"]:
            return {"valid":False, "message":"The book must have publisher", "reference": False}
        if not book_details["published_date"]:
            return {"valid":False, "message":"The book must have published date", "reference": False}
        
        return output
    def pre_update_validation(book_details:dict):
        output = {"valid":True, "message":"The book copy and its details have been added.", "reference": False}
        if not book_details["ISBN"]:
            return {"valid":False, "message":"The book must have ISBN", "reference": False}
        
        if BookDetails.objects.filter(ISBN=book_details["ISBN"]):
            return {"valid":True, "message":"The Book Details have been updated", "reference": True}
        
        if not book_details["title"]:
            return {"valid":False, "message":"The book must have title", "reference": False}
        authors: list = book_details["authors"]
        if not book_details["authors"][0]:
            return {"valid":False, "message":"The book must have authors", "reference": False}
        if not book_details["category"]:
            return {"valid":False, "message":"The book must have category", "reference": False}
        if not book_details["description"]:
            return {"valid":False, "message":"The book must have description", "reference": False}
        if not book_details["publisher"]:
            return {"valid":False, "message":"The book must have publisher", "reference": False}
        if not book_details["published_date"]:
            return {"valid":False, "message":"The book must have published date", "reference": False}
        
        return output


class User(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    birth_date = models.DateField()
    is_admin = models.BooleanField(default=False)
    profile_image_link = models.URLField(blank=True, null=True)
    website_view = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    def is_valid_email(user:dict):
        try:
            validate_email(user["email"])
            return True
        except ValidationError:
            return False
    def pre_add_validation(user:dict, unique_username = True):
        output={"valid": True, "message":"This User is valid to be added"}
        if not User.is_valid_email(user):
            output["valid"]=False
            output["message"]="Please, Enter a valid email address"
            return output

        if(User.objects.filter(username = user["username"]) and unique_username):
            output["valid"]=False
            output["message"]="This username is already existed"
            return output
        return output
    def view_code(key):
        view_codes = {"":0, "Dark":1, "View1":2, "View2": 3}
        if key in view_codes.keys():
            return view_codes[key]
        return -1
    def view_code_reverse(key):
        view_codes = {0:"", 1:"Dark", 2:"View1", 3:"View2"}
        if key in view_codes.keys():
            return view_codes[key]
        return -1
    def validate_permissions(current_token):
        output = {"valid":True, "message":"Permissions are Granted"}
        if current_token:
            current_user = User.objects.filter(username = current_token["username"])
            if current_user:
                current_user = User.objects.get(username = current_token["username"])
                if current_user.password!=current_token["password"]:
                    output = {"valid":False, "message":"Access Denied"}
                
            else:
                output = {"valid":False, "message":"Access Denied"}
        else:
            output = {"valid":False, "message":"User is not signed-in"}
        return output


class BookCopy(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    details = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    printed_date = models.DateField()
    is_available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.details.title} (Copy ID: {self.ID})"
    def pre_add_validation(book_copy: dict, check_unique=True):
        output = {"valid":True, "message":"The copy is valid"}
        if not book_copy["ID"]:
            return {"valid":False, "message":"This copy id must not be empty."}
        if check_unique:
            is_not_unique = BookCopy.objects.filter(ID=book_copy["ID"])
            if(is_not_unique):
                return {"valid":False, "message":"This copy id is already exists"}
            
        if not book_copy["details"]:
           return {"valid":False, "message":"The book should have details. ISBN reference must not be null or empty."}
        if not book_copy["printed_date"]:
           return {"valid":False, "message":"The book should have a print date."}
        return output
