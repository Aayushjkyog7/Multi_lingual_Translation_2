from django.conf import settings
from django.utils import translation

from content_app.models import Video, Moment, Podcast, Article
from content_app.serializers import (
    VideoSerializer,
    MomentSerializer,
    PodcastSerializer,
    ArticleSerializer,
)

CONTENT_MAP = {
    "video": (Video, VideoSerializer),
    "videos": (Video, VideoSerializer),
    "moment": (Moment, MomentSerializer),
    "moments": (Moment, MomentSerializer),
    "podcast": (Podcast, PodcastSerializer),
    "podcasts": (Podcast, PodcastSerializer),
    "article": (Article, ArticleSerializer),
    "articles": (Article, ArticleSerializer),
}


def get_translated_content(*, content_type: str, object_id=None, lang: str = None):
    # Use modeltranslation language configuration so Hindi (`hi`) is treated as supported
    supported = getattr(settings, "MODELTRANSLATION_LANGUAGES", ("en", "hi"))
    default = getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", "en")
    lang = lang or default
    if lang not in supported:
        lang = default

    content_type = (content_type or "").strip().lower()
    if content_type not in CONTENT_MAP:
        raise ValueError(f"Unsupported content type: {content_type}")

    model, serializer_class = CONTENT_MAP[content_type]

    translation.activate(lang)
    try:
        qs = model.objects.all()
        if object_id is not None:
            instance = qs.get(pk=object_id)
            serializer = serializer_class(instance)
            data = serializer.data
        else:
            serializer = serializer_class(qs, many=True)
            data = serializer.data
        return {"language": lang, "content_type": content_type, "data": data}
    finally:
        translation.deactivate()
