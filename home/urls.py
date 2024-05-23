from django.urls import path
from . import views
urlpatterns =[
    path('home/', views.home, name="Home"),
    path('books/', views.books, name="Books"),
    path('account-sign-in/', views.account_sign_in, name="Sign-In"),
    path('account-sign-up/', views.account_sign_up, name="Sign-Up"),
    path('account-sign-in-action/',views.account_sign_in_action, name="Sign-In-Action"),
    path('account-sign-up-action/',views.account_sign_up_action, name="Sign-Up-Action"),
    path('account-update-action/', views.account_update_action, name="Update-Action"),
    path('profile/', views.profile, name="profile"),
    path('profile-change-password/', views.change_password, name="Change-Password"),
]