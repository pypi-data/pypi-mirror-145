# Copyright 2022 Vadim Sharay <vadimsharay@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, Dict, Any

from jsonpath_ng.ext import parse

TYPES_MAP = {
    "object": dict,
    "dict": dict,
    "array": list,
    "list": list,
    "boolean": bool,
    "bool": bool,
    "number": float,
    "int": int,
    "integer": int,
    "float": float,
    "str": str,
    "string": str,
}


def transform(schema: Dict, data: Any, initial_data: Any = None) -> Dict:
    """
    The main function that generates a new data structure according to the schema (JSONPath combination).

    .. code-block:: python

        # Usage example

        schema = {
            "source": "$",  # root data (initial_data)
            "type": "object",
            "properties": {  # fields schema for the new object
                "field1": {
                    "source": "@.field1 * 2",  # JSONPath
                    "type": "float"
                },
                "field2": {
                    "source": "@.array",
                    "type": "array",
                    "items": {
                        "source": "@.number"
                    }
                }
            }
        }

        data = {
            "field1": 1.5,
            "array": [
                {"number": 1},
                {"number": 2}
            ]
        }

        assert transform(schema, data) == {
            "field1": 3.0,
            "field2": [1, 2]
        }

    :param schema: You can create your own data structure according to the schema.
    :param data: Any input data
    :param initial_data: Initial data that will use as root (source: "$"). Default: data param value
    :return: new data with specific structure (according to the schema)
    """
    source = schema.get("source", "")
    default = schema.get("default", data)
    type_name = schema.get("type")

    if type_name and type_name not in TYPES_MAP:
        raise ValueError("Type '{}' is not allowed".format(type_name))

    type_fn = TYPES_MAP[type_name] if type_name else (lambda x: x)  # type: Callable

    if initial_data and "$" in source:
        data = initial_data
    elif not initial_data:
        initial_data = data

    if not source:
        matched_data = default
    else:
        if type_fn == list:
            source += "[:]"

        matched_data = [match.value for match in parse(source).find(data)]

        if type_fn != list:
            matched_data = matched_data[0] if matched_data else None

    if type_fn == dict:
        result_obj = {}
        schema = schema.get("properties")

        if schema is not None:
            if not isinstance(schema, dict):
                raise ValueError("Bad `properties` type: dict expected")

            for field, field_schema in schema.items():
                result_obj[field] = transform(field_schema, matched_data, initial_data)
        else:
            result_obj = dict(matched_data) if matched_data else None

    elif type_fn == list:
        result_obj = []
        schema = schema.get("items")

        if schema is not None:
            if not isinstance(schema, dict):
                raise ValueError("Bad `items` field type: dict expected")

            for item in matched_data:
                result_obj.append(transform(schema, item, initial_data))

        else:
            result_obj = list(matched_data) if matched_data else None

    else:
        result_obj = type_fn(matched_data) if matched_data else None

    return result_obj
