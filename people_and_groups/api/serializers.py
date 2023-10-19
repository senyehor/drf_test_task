from rest_framework import serializers

from people_and_groups.models import Group, Person
from utils.drf.read_only_model_serializer import ReadOnlyModelSerializer


class PersonNoGroupsReadonlySerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class GroupNoMembersReadonlySerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    groups = GroupNoMembersReadonlySerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ('email',)


class GroupSerializer(serializers.ModelSerializer):
    members = PersonNoGroupsReadonlySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
