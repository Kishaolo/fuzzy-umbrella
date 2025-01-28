from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at') #pola dla otobrashenia v spiske objectov
    list_filter = ('created_at',) #filter po date sozdania
    search_fields = ('name',) #poisk po imeni
    ordering = ('-created_at') #sortirovka po date sozdania