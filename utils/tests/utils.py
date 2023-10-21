from django.db.models import Model


def ensure_expected_model_objects_ids_match_serialized_objects_ids_and_count(
        expected_model_objects: list[Model],
        serialized_objects: list[dict]
):
    assertion_error_message = f'model objects do not match serialized objects'
    assert len(expected_model_objects) == len(serialized_objects), assertion_error_message
    model_ids = set(model_object.id for model_object in expected_model_objects)
    serialized_ids = set(data_item['id'] for data_item in serialized_objects)
    assert model_ids == serialized_ids, assertion_error_message
