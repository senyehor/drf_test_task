from rest_framework.serializers import ModelSerializer

from utils.drf.exceptions import SerializerIsReadOnly


class ReadOnlyModelSerializer(ModelSerializer):
    """
    Serializer to allow only data read from instance,
    so due to restricted __init__ interface some errors
    may occur when used for non-read operations
    """

    def __init__(self, instance=None, **kwargs):
        if 'data' in kwargs:
            raise SerializerIsReadOnly
        super().__init__(instance, **kwargs)

    def save(self, **kwargs):
        raise SerializerIsReadOnly

    def create(self, validated_data):
        raise SerializerIsReadOnly

    def update(self, instance, validated_data):
        raise SerializerIsReadOnly
