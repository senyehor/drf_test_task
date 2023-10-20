from django.test import TestCase

from utils.drf.exceptions import SerializerIsReadOnly
from utils.drf.read_only_model_serializer import ReadOnlyModelSerializer


class TestReadOnlyModelSerializer(TestCase):

    def setUp(self) -> None:
        self.__stub_none_instance = None
        self.__stub_none_validated_data = None
        super().setUp()

    def test_non_read_methods_throw_exception(self):
        # despite the intended use to be subclassed, object of class itself
        # is suitable for test purposes, as overridden methods are tested
        serializer = ReadOnlyModelSerializer(self.__stub_none_instance)
        ensure_serializer_is_read_only_is_raised_manager = self.assertRaises(
            SerializerIsReadOnly,
            msg='serializer should raise exception on non-read operation'
        )
        with ensure_serializer_is_read_only_is_raised_manager:
            serializer.save()
        with ensure_serializer_is_read_only_is_raised_manager:
            serializer.create(self.__stub_none_validated_data)
        with ensure_serializer_is_read_only_is_raised_manager:
            serializer.update(self.__stub_none_instance, self.__stub_none_validated_data)

    def test_serializer_does_not_accept_data_argument_for_init(self):
        stub_none_data = None
        ensure_serializer_is_read_only_is_raised = self.assertRaises(
            SerializerIsReadOnly,
            msg='serializer should not accept data argument'
        )
        with ensure_serializer_is_read_only_is_raised:
            ReadOnlyModelSerializer(data=stub_none_data)
        with ensure_serializer_is_read_only_is_raised:
            ReadOnlyModelSerializer(instance=self.__stub_none_instance, data=stub_none_data)
