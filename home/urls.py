from django.urls import path
from . import views
urlpatterns =[
    path('home/', views.home, name="Home"),
    path('books/', views.books, name="Books"),
    path('account-sign-in/', views.account_sign_in, name="Sign-In"),
    path('account-sign-up/', views.account_sign_up, name="Sign-Up"),
]