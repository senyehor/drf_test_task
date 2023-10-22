from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404


def get_object_or_404_with_api_exception(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404 as e:
        error_message = e.args[0]
        raise NotFound(detail=error_message)
