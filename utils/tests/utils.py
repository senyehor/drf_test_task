from typing import Iterable


def make_ids_set_from_serialized_data_objects(data: Iterable[dict]) -> set[int]:
    return set(data_item['id'] for data_item in data)
