# flask-json-pattern

Decorator for REST endpoints in flask. Validate JSON request data.

## Installation

Use pip to install the package:

```bash
pip install flask-json-pattern
```

## Usage

This package provides a flask route decorator to validate json payload.

```python
from flask import Flask, jsonify
from flask_json_pattern import json_pattern

app = Flask(__name__)


@app.route('/greet', methods=['POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str}
})
def greet():
    return jsonify({"msg": "Hello %(name)s %(surname)s" % request.json})
```

## Required fields

By default all fields are required, If you want you can change this behavior by adding `required: False` in the field you want

```python
@app.route('/greet', methods=['POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str, 'required': False}
})
def greet():
    return ""
```

## Default values

When the field is optional `required: False`, you could set the default value of it using the `default` property.

```python
@app.route('/greet', methods=['POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str, "default": 'unknown'}
})
def greet():
    return ""
```

## Empty values

By default the fields can be empty, you could change this if you set the `empty` property to false.

```python
@app.route('/greet', methods=['POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str, "empty": False}
})
def greet():
    return ""
```

Also, you could change the empty and default properties, so that when the property is empty assign a value.

```python
@app.route('/greet', methods=['POST'])
@json_pattern({
    'name': {'type': str,  "empty": False, 'default': "unknown"},
    'surname': {'type': str}
})
def greet():
    return ""
```

## Skip validation methods

If you want to skip the validation for some HTTP methods, can you set `ignore_methods=[]`. By default methods that do not expect a body are GET, HEAD and DELETE.

```python
@app.route('/greet', methods=['GET', 'POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str}
}, ignore_methods=['GET'])
def greet():
    return ""
```

## Tuple and list

If you want, you can validate the data type of each position of a simple list

```python
@app.route('/greet', methods=['GET', 'POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str},
    'skills': {
        'type': list,
        'of': str
    }
}, ignore_methods=['GET'])
def greet():
    return ""
```

Also, If you want you could validate lists of objects, and the fields of each object.

```python
@app.route('/greet', methods=['GET', 'POST'])
@json_pattern({
    'name': {'type': str},
    'surname': {'type': str},
    'skills': {
        'type': list,
        "schema": {
            "name": {"type": str}
        }
    }
}, ignore_methods=['GET'])
def greet():
    return ""
```

## Error handling

On validation failure the library calls `flask.abort` and passes an 400 error code and instance of the ValidationError.

```python
from flask import make_response, jsonify
from flask_json_pattern import ValidationError

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        return make_response(jsonify({'msg': error.description.message}), 400)
    return error
```