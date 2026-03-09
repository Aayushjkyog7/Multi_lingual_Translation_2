from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from .models import Video, Moment, Podcast, Article
from .serializers import VideoSerializer, MomentSerializer, PodcastSerializer, ArticleSerializer

@api_view(['GET'])
def content_types(request):
    """Return list of available content types"""
    # Return identifiers - translation happens on frontend
    return Response({
        'contentTypes': ['videos', 'moments', 'podcasts', 'articles']
    })


@api_view(['GET'])
def get_content(request, content_type):
    """Return content data for a specific content type"""
    content_type = content_type.lower()
    
    # Get language from query parameter; validate against supported locales (see settings.SUPPORTED_LOCALES)
    supported = getattr(settings, 'SUPPORTED_LOCALES', ('en',))
    default = getattr(settings, 'DEFAULT_LOCALE', 'en')
    lang = request.GET.get('lang', default)
    if lang not in supported:
        lang = default
    
    # Activate language for translations (Video and Moment models use translated title/description)
    translation.activate(lang)
    
    try:
        if content_type == 'videos':
            items = Video.objects.all()
            serializer = VideoSerializer(items, many=True)
        elif content_type == 'moments':
            items = Moment.objects.all()
            serializer = MomentSerializer(items, many=True)
        elif content_type == 'podcasts':
            items = Podcast.objects.all()
            serializer = PodcastSerializer(items, many=True)
        elif content_type == 'articles':
            items = Article.objects.all()
            serializer = ArticleSerializer(items, many=True)
        else:
            return Response(
                {'error': _('Invalid content type')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({'data': serializer.data, 'language': lang})
    finally:
        # Reset to default language
        translation.deactivate()