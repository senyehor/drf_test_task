from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from people_and_groups.api.permissions import IsAdminElseReadOnly
from people_and_groups.api.serializers import GroupSerializer, PersonSerializer
from people_and_groups.logic.simple import (
    add_person_to_group_with_membership_check, remove_person_from_group_with_membership_check,
)
from people_and_groups.models import Group, Person
from utils.drf.get_object_or_404_with_api_exception import get_object_or_404_with_api_exception
from utils.drf.views import ModelViewSetWithSeparateCreateUrl


class PersonViewSet(ModelViewSetWithSeparateCreateUrl):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminElseReadOnly]

    @action(methods=('POST',), detail=True, url_path='add-group', url_name='add-group')
    def add_person_to_group(self, *args, **kwargs):
        person = self.get_object()
        group = get_object_or_404_with_api_exception(
            Group,
            id=self.request.data['group_id']
        )
        add_person_to_group_with_membership_check(person, group)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('POST',), detail=True, url_path='remove-group', url_name='remove-group')
    def remove_person_from_group(self, *args, **kwargs):
        person = self.get_object()
        group = get_object_or_404_with_api_exception(
            Group,
            id=self.request.data['group_id']
        )
        remove_person_from_group_with_membership_check(person, group)
        return Response(status=status.HTTP_200_OK)


class GroupViewSet(ModelViewSetWithSeparateCreateUrl):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminElseReadOnly]
