from django.contrib import admin

# Register your models here.
from .models import UserModel


# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "username",
        "image_path",
        "created_at",
        "updated_at",
        "is_superuser",
    ]
