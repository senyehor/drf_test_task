from rest_framework.exceptions import APIException


class EmailIsReadOnly(APIException):
    status_code = 400
    default_detail = 'Email can not be updated'
    default_code = 'email_read_only'
