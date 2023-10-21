from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from people_and_groups.models import Person
from people_and_groups.tests.factories import GroupFactory, PersonFactory
from utils.tests.factories import UserFactory
from utils.tests.utils import \
    ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count


class TestPersonCrud(TestCase):
    def setUp(self):
        admin = UserFactory(is_staff=True)
        self.__admin_client = APIClient()
        self.__admin_client.force_authenticate(admin)

    def test_create_person(self):
        person = PersonFactory.build()
        correct_person_data = {
            'name':    person.name,
            'surname': person.surname,
            'email':   person.email
        }
        response = self.__admin_client.post(
            reverse('person-list'),
            data=correct_person_data
        )
        self.assertEquals(
            response.status_code, status.HTTP_201_CREATED,
            'invalid response code'
        )
        try:
            Person.objects.get(
                **correct_person_data
            )
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            assert False, f'failed to retrieve created person, {e}'

    def test_retrieve_person(self):
        person = PersonFactory()
        groups_for_person = [GroupFactory() for _ in range(5)]
        person.groups.set(groups_for_person)
        response = self.__admin_client.get(
            reverse('person-detail', kwargs={'pk': person.id}),
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        parsed_response = response.json()
        self.assertEquals(
            person.id, parsed_response['id'],
            'person data does not match expected'
        )
        self.assertEquals(
            person.name, parsed_response['name'],
            'person data does not match expected'
        )
        self.assertEquals(
            person.surname, parsed_response['surname'],
            'person data does not match expected'
        )
        ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
            groups_for_person,
            parsed_response['groups']
        )

    def test_retrieve_people(self):
        some_people = [PersonFactory() for _ in range(5)]
        response = self.__admin_client.get(
            reverse('person-list')
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'invalid response code'
        )
        ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
            some_people,
            response.json()
        )

    def test_update_person_name_and_surname(self):
        person = PersonFactory()
        new_data_without_email = {
            'name':    'new_name',
            'surname': 'new_surname'
        }
        response = self.__admin_client.patch(
            reverse('person-detail', kwargs={'pk': person.id}),
            data=new_data_without_email
        )
        self.assertEquals(
            response.status_code, status.HTTP_200_OK,
            'failed to update person'
        )
        person.refresh_from_db()
        self.assertEquals(
            person.name, new_data_without_email['name'],
            'person name was not updated'
        )
        self.assertEquals(
            person.surname, new_data_without_email['surname'],
            'person surname was not updated'
        )

    def test_update_person_email(self):
        person = PersonFactory()
        new_person_email = PersonFactory.build().email
        new_email_data = {'email': new_person_email}
        response = self.__admin_client.patch(
            reverse('person-detail', kwargs={'pk': person.id}),
            data=new_email_data
        )
        self.assertEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'attempt to update email should return bad request'
        )
        person.refresh_from_db()
        self.assertNotEquals(
            person.email, new_person_email,
            'email was updated'
        )

    def test_delete_person(self):
        person_id = PersonFactory().id
        response = self.__admin_client.delete(
            reverse('person-detail', kwargs={'pk': person_id})
        )
        self.assertEquals(
            response.status_code, status.HTTP_204_NO_CONTENT,
            'invalid response code'
        )
        with self.assertRaises(
                ObjectDoesNotExist,
                msg='person was not deleted'
        ):
            Person.objects.get(id=person_id)
