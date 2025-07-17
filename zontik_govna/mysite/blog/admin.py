from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] #spisok oznochaet kakie pola nado videt na paneli ypravlenia adminkoi
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulateds_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarcy = 'publish'
    ordering = ['status', 'publish']
