from django.contrib.auth.models import User
from factory import Sequence
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    is_active = True
    username = Sequence(lambda n: f'username_{n}')
