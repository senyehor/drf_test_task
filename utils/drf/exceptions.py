from rest_framework import status
from rest_framework.exceptions import APIException


class BaseDjangoRestFrameworkUtilityException(Exception):
    pass


class SerializerIsReadOnly(BaseDjangoRestFrameworkUtilityException):
    pass


class DataNotProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Some data was not provided'
    default_code = 'some_data_not_provided'

    __detail_template = '{data_name} was not provided'

    def __init__(self, data_name: str):
        self.default_detail = self.__detail_template.format(data_name=data_name)
