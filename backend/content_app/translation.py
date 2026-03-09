from modeltranslation.translator import register, TranslationOptions
from .models import Video, Moment


@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Moment)
class MomentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

