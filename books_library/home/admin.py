from django.contrib import admin
from .models import User, BookCopy, BookDetails
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","full_name", "email", "is_admin")
class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ("ISBN", "title","category","publisher","published_date")
    

class BookCopyAdmin(admin.ModelAdmin):
    list_display = ("get_title", "ID", "printed_date","is_available","borrowed_by","due_date")
    def get_title(self, copy):
        return copy.details.title
    
admin.site.register(User, UserAdmin)

admin.site.register(BookCopy, BookCopyAdmin)
admin.site.register(BookDetails, BookDetailsAdmin)