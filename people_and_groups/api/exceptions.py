from rest_framework import status
from rest_framework.exceptions import APIException


class EmailIsReadOnly(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Email can not be updated'
    default_code = 'email_read_only'
