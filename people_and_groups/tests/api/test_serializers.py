from django.test import TestCase

from people_and_groups.api.exceptions import EmailIsReadOnly
from people_and_groups.api.serializers import (
    GroupSerializer, PersonNoGroupsReadonlySerializer,
    PersonSerializer,
)
from people_and_groups.tests.factories import GroupFactory, PersonFactory
from utils.tests.utils import make_ids_set_from_serialized_data_objects


class TestPersonSerializers(TestCase):

    def setUp(self) -> None:
        self.__person = PersonFactory()
        self.__groups = [GroupFactory() for _ in range(5)]
        for group in self.__groups:
            group.members.add(self.__person)
            group.save()
        super().setUp()

    def test_groups_in_serialized_person(self):
        person_serialized_data = PersonSerializer(self.__person).data
        groups_data = person_serialized_data['groups']
        self.assertEquals(
            len(groups_data),
            len(self.__groups),
            'serializer returned wrong group count'
        )
        group_from_serialized_data_ids = make_ids_set_from_serialized_data_objects(groups_data)
        expected_group_ids = set(group.id for group in self.__groups)
        self.assertEquals(
            expected_group_ids, group_from_serialized_data_ids,
            'serializer returned wrong groups'
        )

    def test_person_no_groups_read_only_serializer_serialization(self):
        expected_fields = ('id', 'name', 'surname', 'email')
        serializer = PersonNoGroupsReadonlySerializer(self.__person)
        serialized_data = serializer.data
        for field_name in expected_fields:
            try:
                self.assertEquals(
                    serialized_data[field_name],
                    getattr(self.__person, field_name),
                    f'field {field_name} does not match field in serialized data'
                )
            except AttributeError:
                assert False, f'some field from serialized data was not found in person object'

    def test_updating_email(self):
        new_email = PersonFactory.build().email
        serializer = PersonSerializer(self.__person, data={'email': new_email})
        self.assertTrue(
            serializer.is_valid(),
            'serializer invalid with correct email'
        )
        with self.assertRaises(
                EmailIsReadOnly,
                msg='email should not be updated'
        ):
            serializer.save()


class TestGroupSerializers(TestCase):
    def setUp(self) -> None:
        self.__group = GroupFactory()
        self.__members = [PersonFactory() for _ in range(5)]
        self.__group.members.set(self.__members)
        super().setUp()

    def test_members_in_serialized_group(self):
        group_serialized_data = GroupSerializer(self.__group).data
        members_data = group_serialized_data['members']
        self.assertEquals(
            len(self.__members),
            len(members_data),
            'invalid member count in group serialized data'
        )
        member_ids_from_serialized_data = make_ids_set_from_serialized_data_objects(members_data)
        actual_member_ids = set(member.id for member in self.__members)
        self.assertEquals(
            member_ids_from_serialized_data, actual_member_ids,
            'group serializer returned wrong members'
        )
