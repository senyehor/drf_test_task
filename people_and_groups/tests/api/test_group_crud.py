from random import randint, seed
from time import time

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from people_and_groups.models import Group
from people_and_groups.tests.factories import GroupFactory, PersonFactory
from utils.tests.drf.utils import create_admin_client
from utils.tests.utils import \
    ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count


class TestGroupCrud(TestCase):
    def setUp(self) -> None:
        seed(time())
        self.__admin_client = create_admin_client()
        group = GroupFactory.build()
        self.__correct_group_data = {
            'name': group.name
        }
        super().setUp()

    def test_create_group(self):
        # delete all objects to ensure no group with the same name
        # messes up test
        Group.objects.all().delete()
        response = self.__admin_client.post(
            reverse('group-create'),
            data=self.__correct_group_data
        )
        self.assertEquals(
            response.status_code, status.HTTP_201_CREATED,
            'invalid response code'
        )
        try:
            Group.objects.get(name=self.__correct_group_data['name'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            assert False, 'group was not created correctly'

    def test_retrieve_group(self):
        group = GroupFactory()
        members = [PersonFactory() for _ in range(5)]
        group.members.set(members)
        response = self.__admin_client.get(
            reverse('group-detail', kwargs={'pk': group.id}),
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid status code'
        )
        group_data = response.json()
        self.assertEquals(
            group.id, group_data['id'],
            'group id does not match'
        )
        received_group_members = group_data['members']
        ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
            members, received_group_members
        )

    def test_retrieve_groups(self):
        groups = [GroupFactory() for _ in range(5)]
        members_of_groups = []
        for group in groups:
            members = [
                PersonFactory()
                for _ in range(randint(3, 6))
            ]
            group.members.set(members)
            members_of_groups.append(members)
        response = self.__admin_client.get(
            reverse('group-list')
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        groups_data = response.json()
        ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
            groups, groups_data
        )
        for group_data in groups_data:
            group_id = group_data['id']
            corresponding_group = Group.objects.get(id=group_id)
            group_members = corresponding_group.members.all()
            received_group_members_serialized = group_data['members']
            ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
                group_members, received_group_members_serialized
            )

    def test_update_group(self):
        group = GroupFactory()
        new_data = {'name': GroupFactory.build().name}
        response = self.__admin_client.patch(
            reverse('group-detail', kwargs={'pk': group.id}),
            data=new_data
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        group.refresh_from_db()
        self.assertEquals(
            group.name, new_data['name'],
            'group name was not updated'
        )

    def test_delete_group(self):
        group = GroupFactory()
        response = self.__admin_client.delete(
            reverse('group-detail', kwargs={'pk': group.id}),
        )
        self.assertEquals(
            response.status_code, status.HTTP_204_NO_CONTENT,
            'invalid response code'
        )
        with self.assertRaises(
                ObjectDoesNotExist,
                msg='group was not deleted'
        ):
            Group.objects.get(id=group.id)
