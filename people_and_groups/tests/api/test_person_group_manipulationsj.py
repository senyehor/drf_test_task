from django.test import TestCase
from django.urls import reverse

from people_and_groups.tests.factories import GroupFactory, PersonFactory
from utils.tests.drf.utils import create_admin_client


class TestPersonGroupManipulations(TestCase):

    def setUp(self) -> None:
        self.__person = PersonFactory()
        self.__admin_client = create_admin_client()
        super().setUp()

    def test_adding_group(self):
        group = GroupFactory()
        response = self.__admin_client.post(
            reverse('person-add-group', kwargs={'pk': self.__person.id}),
            data={'group_id': 33}
        )
        print('a')
