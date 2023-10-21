from unittest.mock import Mock

from django.test import TestCase

from people_and_groups.api.permissions import IsAdminElseReadOnly
from utils.tests.factories import UserFactory


class TestIsAdminElseReadOnlyPermission(TestCase):
    ALLOWED_READ_ONLY_METHODS_FOR_NON_ADMIN_USERS = ('GET', 'OPTIONS', 'HEAD')
    ADMIN_ONLY_METHODS = ('POST', 'PUT', 'DELETE', 'PATCH')

    def setUp(self) -> None:
        self.__non_admin_user = UserFactory(is_staff=False)
        self.__admin_user = UserFactory(is_staff=True)
        self.__request_mock = Mock(spec_set=('method', 'user'))
        super().setUp()

    def test_for_non_admin(self):
        for method in self.ALLOWED_READ_ONLY_METHODS_FOR_NON_ADMIN_USERS:
            self.__request_mock.method = method
            self.__request_mock.user = self.__non_admin_user
            # noinspection PyTypeChecker
            self.assertTrue(
                IsAdminElseReadOnly().has_permission(self.__request_mock, None),
                f'non-admin user should have permission to read for {method}'
            )
        for method in self.ADMIN_ONLY_METHODS:
            self.__request_mock.method = method
            self.__request_mock.user = self.__non_admin_user
            # noinspection PyTypeChecker
            self.assertFalse(
                IsAdminElseReadOnly().has_permission(self.__request_mock, None),
                f'non-admin user should not have permission for {method}'
            )

    def test_for_admin(self):
        all_methods = [
            *self.ALLOWED_READ_ONLY_METHODS_FOR_NON_ADMIN_USERS,
            *self.ADMIN_ONLY_METHODS
        ]
        for method in all_methods:
            self.__request_mock.method = method
            self.__request_mock.user = self.__admin_user
            # noinspection PyTypeChecker
            self.assertTrue(
                IsAdminElseReadOnly().has_permission(self.__request_mock, None),
                f'admin user should have permission for {method}'
            )
