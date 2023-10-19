from django.db import models


class Person(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default=None
    )
    surname = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default=None
    )
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        default=None
    )


class Group(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    members = models.ManyToManyField(
        Person,
        related_name='groups'
    )
