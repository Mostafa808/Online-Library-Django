from django.db import models
from django.utils import timezone

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

class BookCopy(models.Model):
    ID = models.CharField(max_length=20, primary_key=True)
    details = models.ForeignKey(BookDetails, on_delete=models.CASCADE)
    printed_date = models.DateField()
    is_available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.details.title} (Copy ID: {self.ID})"
