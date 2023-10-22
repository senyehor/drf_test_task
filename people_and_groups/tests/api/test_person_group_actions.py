from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from people_and_groups.logic.exceptions import PersonAlreadyInThisGroup, PersonNotInThisGroup
from people_and_groups.tests.factories import GroupFactory, PersonFactory
from utils.tests.drf.utils import create_admin_client


class TestPersonGroupActions(TestCase):

    def setUp(self) -> None:
        self.__person = PersonFactory()
        self.__group = GroupFactory()
        self.__admin_client = create_admin_client()
        super().setUp()

    def test_add_group(self):
        response = self.__admin_client.post(
            reverse('person-add-group', kwargs={'pk': self.__person.id}),
            data={'group_id': self.__group.id}
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        self.assertIn(
            self.__group,
            self.__person.groups.all(),
            'person was not added to the group'
        )

    def test_add_group_which_person_is_already_in(self):
        self.__group.members.add(self.__person)
        response = self.__admin_client.post(
            reverse('person-add-group', kwargs={'pk': self.__person.id}),
            data={'group_id': self.__group.id}
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

    def test_remove_person_from_group(self):
        self.__group.members.add(self.__person)
        response = self.__admin_client.post(
            reverse('person-remove-group', kwargs={'pk': self.__person.id}),
            data={'group_id': self.__group.id}
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        self.assertNotIn(
            self.__group,
            self.__person.groups.all(),
            'person was not removed from the group'
        )

    def test_remove_person_from_group_where_he_is_not_in(self):
        response = self.__admin_client.post(
            reverse('person-remove-group', kwargs={'pk': self.__person.id}),
            data={'group_id': self.__group.id}
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
