from rest_framework.test import APIClient

from utils.tests.factories import UserFactory


def create_admin_client() -> APIClient:
    admin = UserFactory(is_staff=True)
    client = APIClient()
    client.force_authenticate(admin)
    return client
