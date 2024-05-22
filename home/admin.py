from django.contrib import admin
from .models import User, BookCopy, BookDetails
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","full_name", "email", "is_admin")
admin.site.register(User, UserAdmin)
#admin.site.register(BookCopy, AdminUser)
#admin.site.register(BookDetails, AdminUser)