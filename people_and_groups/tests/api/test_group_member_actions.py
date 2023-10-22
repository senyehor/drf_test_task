from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from people_and_groups.logic.exceptions import PersonAlreadyInThisGroup, PersonNotInThisGroup
from people_and_groups.tests.factories import GroupFactory, PersonFactory
from utils.tests.drf.utils import create_admin_client
from utils.tests.utils import \
    ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count


class TestGroupMemberActions(TestCase):
    def setUp(self) -> None:
        self.__group = GroupFactory()
        self.__admin_client = create_admin_client()
        super().setUp()

    def test_get_members(self):
        members = [PersonFactory() for _ in range(5)]
        self.__group.members.set(members)
        response = self.__admin_client.get(
            reverse('group-members', kwargs={'pk': self.__group.id})
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        serialized_members = response.json()['members']
        ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
            members, serialized_members
        )

    def test_add_member(self):
        person = PersonFactory()
        response = self.__admin_client.post(
            reverse('group-add-member', kwargs={'pk': self.__group.id}),
            data={'person_id': person.id}
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        self.assertIn(
            person, self.__group.members.all(),
            'person was not added to group'
        )

    def test_add_duplicate_member(self):
        person = PersonFactory()
        self.__group.members.add(person)
        response = self.__admin_client.post(
            reverse('group-add-member', kwargs={'pk': self.__group.id}),
            data={'person_id': person.id}
        )
        self.assertEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'invalid response code'
        )
        self.assertEquals(
            response.json()['detail'],
            PersonAlreadyInThisGroup.default_detail,
            'wrong error message'
        )

    def test_remove_member(self):
        person = PersonFactory()
        self.__group.members.add(person)
        response = self.__admin_client.post(
            reverse('group-remove-member', kwargs={'pk': self.__group.id}),
            data={'person_id': person.id}
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        self.assertNotIn(
            person, self.__group.members.all(),
            'member was not removed from group'
        )

    def test_remove_member_who_is_not_in_group(self):
        person = PersonFactory()
        response = self.__admin_client.post(
            reverse('group-remove-member', kwargs={'pk': self.__group.id}),
            data={'person_id': person.id}
        )
        self.assertEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'invalid response code'
        )
        self.assertEquals(
            response.json()['detail'],
            PersonNotInThisGroup.default_detail,
            'wrong error message'
        )
