from flask import request, abort
from functools import wraps
from bson import ObjectId
from .validator import ValidationError


def __set_default_value(key: str, spec: dict, body: dict, err_msg: str) -> bool:
    if 'default' in spec:  # si tiene valor por default
        body.update({key: spec['default']})
    elif err_msg:
        abort(400, ValidationError(err_msg))


def valid_schema(nav: list, schema: dict, rbody: dict):
    for key, spec in schema.items():
        prop = '.'.join((*nav, key))
        # si especifica que tenga tipo
        tps = [dict, ]  # por defecto es object
        if spec.get('type', False):
            tps = list(spec['type']) if isinstance(spec['type'], (tuple, list)) else [spec['type'], ]
            tps = [tp for tp in tps if tp is not None]
        if key in rbody.keys():
            flgs = False  # tipo encontrado
            for tp in tps:  # recorre cada tipo
                if tp.__name__ == 'ObjectId':  # si va a ser del tipo ObjectId
                    # si ya es un objectId, lo omite
                    if isinstance(rbody[key], ObjectId) is True:
                        pass
                    elif bool(rbody[key]) is True:  # otro tipo y si tiene dato
                        try:  # intenta hacer casteo
                            rbody.update({key: ObjectId(rbody[key])})
                        except:
                            break
                    elif spec.get('empty', True) is False:
                        abort(400, ValidationError("%s can't be empty" % prop))
                    flgs = True
                    break
                # demas tipos
                elif isinstance(rbody[key], tp) is True:
                    flgs = True
                    # si no debe estar vacio y lo esta
                    if spec.get('empty', True) is False and bool(rbody[key]) is False:
                        __set_default_value(key, spec, rbody, "%s can't be empty" % prop)
                    break
            # si no encontro un tipo valido
            if flgs is False:
                abort(400, ValidationError("%s must be an instance of (%s)" % (prop, ','.join([tp.__name__ for tp in tps]))))
        # si no existe y es requerido
        elif spec.get('required', True) is True:
            # de no existir y ser requerido,
            # verifica si tiene default
            __set_default_value(key, spec, rbody, "%s is missing" % prop)
        # de no existir, pero tiene valor por defecto
        # crea el campo y no aborta la solicitud
        else:
            __set_default_value(key, spec, rbody, None)
        # si es esquema o tipo
        if 'schema' in spec:
            nav.append(key)
            if any([1 for tp in tps if tp in (object, dict)]):
                valid_schema(nav, spec['schema'], rbody[key])
            elif any([1 for tp in tps if tp in (list, tuple)]):
                for index, item in enumerate(rbody.get(key, [])):
                    nav.append(str(index))
                    valid_schema(nav, spec['schema'], item)
            else:
                raise Exception("schema must be an instance of (list, tuple, dict, object)")
        elif 'of' in spec:
            vls = rbody[key]
            if isinstance(vls, (tuple, list)):
                for index, item in enumerate(vls):
                    if isinstance(item, spec['of']) is False:
                        abort(400, ValidationError("%s.%s must be an instance of %s" % (prop, index, spec['of'])))
            else:
                raise Exception("of must be an instance of (list, tuple)")


def json_pattern(schema: dict = None, ignore_methods: tuple = ("GET", "HEAD", "DELETE")):
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # evalua header que sea de tipo json
            if request.headers['Content-Type'] != 'application/json':
                abort(400, ValidationError("Content-Type of the request has to be 'application/json'"))
            # metodos que por definicion no contienen un cuerpo
            if request.method in ignore_methods:
                return f(*args, **kwargs)
            else:
                rbody = request.json or dict()
                valid_schema([], schema, rbody)
                return f(*args, **kwargs)
        return wrapper
    return inner_function
