from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet


class ModelViewSetWithSeparateCreateUrl(ModelViewSet):
    @action(methods=('POST',), detail=False, url_path='create', url_name='create')
    def create_with_correct_url_name(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
