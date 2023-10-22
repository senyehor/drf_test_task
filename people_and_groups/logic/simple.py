from people_and_groups.logic.exceptions import PersonAlreadyInThisGroup, PersonNotInThisGroup
from people_and_groups.models import Group, Person


def check_person_is_group_member(person: Person, group: Group) -> bool:
    return person in group.members.all()


def add_person_to_group_with_membership_check(person: Person, group: Group):
    if person in group.members.all():
        raise PersonAlreadyInThisGroup
    group.members.add(person)


def remove_person_from_group_with_membership_check(person: Person, group: Group):
    if person not in group.members.all():
        raise PersonNotInThisGroup
    group.members.remove(person)
