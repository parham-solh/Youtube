from django.contrib import admin
from .models import VIDEO,Category,Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ["title","created_at"]
  prepopulated_fields = {"slug": ["title"]}


class CommentAdmin(admin.TabularInline):
  model = Comment
  extra = 1



@admin.register(VIDEO)
class VideoAdmin(admin.ModelAdmin):
  list_display = ["title","thumbnail","category","created_at"]

