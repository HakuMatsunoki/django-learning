from django.contrib import admin

from .models import Company


# Register your models here.
@admin.register(Company)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at", "updated_at", "visible"]
    list_filter = ["visible", "created_at", "updated_at"]
    search_fields = ["name", "description", "visible"]
    raw_id_fields = ["owner"]
