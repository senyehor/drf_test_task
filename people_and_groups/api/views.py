from people_and_groups.api.permissions import IsAdminElseReadOnly
from people_and_groups.api.serializers import GroupSerializer, PersonSerializer
from people_and_groups.models import Group, Person
from utils.drf.views import ModelViewSetWithSeparateCreateUrl


class PersonViewSet(ModelViewSetWithSeparateCreateUrl):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminElseReadOnly]


class GroupViewSet(ModelViewSetWithSeparateCreateUrl):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminElseReadOnly]
