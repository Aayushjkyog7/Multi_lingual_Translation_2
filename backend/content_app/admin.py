from django.contrib import admin
from .models import Video, Moment, Podcast, Article


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'video_id']
    search_fields = ['title', 'description']
    list_filter = ['video_id']


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'moment_id']
    search_fields = ['title', 'description']
    list_filter = ['moment_id']


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'podcast_id']
    search_fields = ['title', 'description']
    list_filter = ['podcast_id']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'article_id']
    search_fields = ['title', 'description']
    list_filter = ['article_id']

