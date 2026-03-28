from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view  # type: ignore[reportMissingImports]
from rest_framework.response import Response  # type: ignore[reportMissingImports]
from rest_framework import status  # type: ignore[reportMissingImports]
from django.utils.translation import gettext as _

from .services.translation_service import get_translated_content


@api_view(["GET"])
def content_types(request):
    return Response({
        "contentTypes": ["videos", "moments", "podcasts", "articles"],
    })


@api_view(["GET"])
def get_content(request, content_type):
    lang = request.GET.get("lang")
    object_id = request.GET.get("id")
    if object_id is not None:
        try:
            object_id = int(object_id)
        except (TypeError, ValueError):
            object_id = None

    try:
        payload = get_translated_content(
            content_type=content_type,
            object_id=object_id,
            lang=lang,
        )
    except ValueError as exc:
        return Response(
            {"error": _("Invalid content type") if "content type" in str(exc).lower() else str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except ObjectDoesNotExist:
        return Response({"error": _("Not found")}, status=status.HTTP_404_NOT_FOUND)

    return Response(payload)