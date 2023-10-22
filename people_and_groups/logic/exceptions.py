from rest_framework import status
from rest_framework.exceptions import APIException

from utils.exceptions import BaseLogicException

_LOGIC_EXCEPTIONS_MERGED_WITH_API_EXCEPTIONS_DOCSTRING = \
    'in order to avoid exceptions duplicity, ' \
    'this exception is a logic exception and an api exception'


class PeopleAndGroupsLogicException(BaseLogicException):
    pass


class PersonAlreadyInThisGroup(PeopleAndGroupsLogicException, APIException):
    __doc__ = _LOGIC_EXCEPTIONS_MERGED_WITH_API_EXCEPTIONS_DOCSTRING
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Person is already a group member'
    default_code = 'person_is_already_in_this_group'


class PersonNotInThisGroup(PeopleAndGroupsLogicException, APIException):
    __doc__ = _LOGIC_EXCEPTIONS_MERGED_WITH_API_EXCEPTIONS_DOCSTRING
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Person is not this group member'
    default_code = 'person_is_not_in_this_group'
