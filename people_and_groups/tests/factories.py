import factory
from factory.django import DjangoModelFactory

from people_and_groups.models import Group, Person


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    name = factory.Sequence(lambda number: f'person_name_{number}')
    surname = factory.Sequence(lambda number: f'surname_{number}')
    email = factory.LazyAttribute(lambda person: f'{person.name}.{person.surname}@example.com')


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda number: f'group_name_{number}')


def create_group_with_members(members_count: int) -> Group:
    members = [PersonFactory() for i in range(members_count)]
    group = GroupFactory()
    group.members.set(members)
    return group
