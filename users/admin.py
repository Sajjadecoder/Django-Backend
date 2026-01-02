from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "full_name")
    ordering = ("email",)
