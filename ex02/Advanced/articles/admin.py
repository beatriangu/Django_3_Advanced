# articles/admin.py
from django.contrib import admin
from .models import Article, Favourite

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'synopsis')
    search_fields = ('title', 'synopsis')

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')
    search_fields = ('user__username', 'article__title')
