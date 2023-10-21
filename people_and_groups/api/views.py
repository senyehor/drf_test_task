from rest_framework.viewsets import ModelViewSet

from people_and_groups.api.permissions import IsAdminElseReadOnly
from people_and_groups.api.serializers import PersonSerializer
from people_and_groups.models import Person


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminElseReadOnly]
