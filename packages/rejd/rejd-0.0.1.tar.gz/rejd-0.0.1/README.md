<!--
 Copyright 2022 Vadim Sharay <vadimsharay@gmail.com>

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -->

# ReJD

ReJD (Representation JSON Data) - Python library that changes your "JSON-like" data representation.

The small library will help you pull data from an input object using JSONPath and
generate new objects according to a schema.

JSONPath is like XPath (XML) for JSON.
To learn the syntax, read the documentation for the [original article](http://goessner.net/articles/JsonPath/).


## Installation

`pip install rejd`

Or you can install it from GitHub:

`pip install -e git+https://github.com/rejd-tools/rejd-python.git`

## Usage example

```
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
```

## Testing

Just run `pytest` to run unit tests.

Or you can use pre-commit to check and fix any issues: `pre-commit run --all`

## License

Apache License 2.0 (See [LICENSE](https://github.com/rejd-tools/rejd-python/blob/master/LICENSE/))
