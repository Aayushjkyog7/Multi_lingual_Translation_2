from rest_framework import serializers
from .models import Video, Moment, Podcast, Article


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_id']
    
    def to_representation(self, instance):
        """Override to return translated title based on current language"""
        representation = super().to_representation(instance)
        # django-modeltranslation automatically handles translation based on current language
        # instance.title will return the translated version based on translation.get_language()
        # So we can just use the default representation
        return representation


class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = ['id', 'title', 'description', 'moment_id']

    def to_representation(self, instance):
        """django-modeltranslation returns translated title/description based on active language"""
        return super().to_representation(instance)


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['id', 'title', 'description', 'podcast_id']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'article_id']

