from typing import Any

from utils.drf.exceptions import DataNotProvided


def get_data_from_dict_with_verbose_api_exception(data: dict, data_key: Any) -> Any:
    if value := data.get(data_key, None):
        return value
    raise DataNotProvided(data_key)
