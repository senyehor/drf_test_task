from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from people_and_groups.api.permissions import IsAdminElseReadOnly
from people_and_groups.api.serializers import (
    GroupNoMembersReadonlySerializer, GroupSerializer,
    PersonSerializer,
)
from people_and_groups.logic.simple import (
    add_person_to_group_with_membership_check, remove_person_from_group_with_membership_check,
)
from people_and_groups.models import Group, Person
from utils.drf.get_data_from_dict_with_verbose_api_exception import \
    get_data_from_dict_with_verbose_api_exception
from utils.drf.get_object_or_404_with_api_exception import get_object_or_404_with_api_exception
from utils.drf.views import ModelViewSetWithSeparateCreateUrl


class PersonViewSet(ModelViewSetWithSeparateCreateUrl):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminElseReadOnly]


class PersonGroupActionsViewSet(GenericViewSet):
    queryset = Person.objects.all()
    permission_classes = [IsAdminElseReadOnly]

    @action(methods=('GET',), detail=True, url_path='groups', url_name='groups')
    def get_person_groups(self, *args, **kwargs):
        person = self.get_object()
        groups = person.groups.all()
        groups_serialized = GroupNoMembersReadonlySerializer(
            groups,
            many=True,
        ).data
        return Response(status=status.HTTP_200_OK, data={'groups': groups_serialized})

    @action(methods=('POST',), detail=True, url_path='add-group', url_name='add-group')
    def add_person_to_group(self, *args, **kwargs):
        person, group = self.__get_person_and_group()
        add_person_to_group_with_membership_check(person, group)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('POST',), detail=True, url_path='remove-group', url_name='remove-group')
    def remove_person_from_group(self, *args, **kwargs):
        person, group = self.__get_person_and_group()
        remove_person_from_group_with_membership_check(person, group)
        return Response(status=status.HTTP_200_OK)

    def __get_person_and_group(self) -> tuple[Person, Group]:
        person = self.get_object()
        group_id = get_data_from_dict_with_verbose_api_exception(
            self.request.data, 'group_id'
        )
        group = get_object_or_404_with_api_exception(
            Group,
            id=group_id
        )
        return person, group


class GroupViewSet(ModelViewSetWithSeparateCreateUrl):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminElseReadOnly]
