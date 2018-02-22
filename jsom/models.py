class ModelMeta(type):
    # For now, pytest starts covering after the tests get collected, therefore
    # it's not able to cover this metaclass. As soon as we fix it, and have
    # the module loaded after coverage is already running, we can remove
    # the "pragma: no cover" below.
    def __init__(cls, name, bases, attr_dict):  # pragma: no cover
        for key, attr in attr_dict.items():
            if isinstance(attr, Field) and attr._name is None:
                attr._name = key


class Model:
    __metaclass__ = ModelMeta

    @classmethod
    def as_schema(cls):
        schema_data = {
            'type': 'object',
            'properties': {},
        }

        fields = (
            (k, v) for (k, v) in cls.__dict__.items()
            if isinstance(v, Field)
        )

        for k, v in fields:
            if v.required:
                schema_data.setdefault('required', [])
                schema_data['required'].append(k)
            schema_data['properties'][k] = {
                'type': v.SCHEMA_TYPE,
            }

        return schema_data

    @classmethod
    def create(cls, **kwargs):
        instance = cls()
        for k, v in kwargs.items():
            if k not in cls.__dict__:
                raise AttributeError('Invalid field: {}'.format(k))
            setattr(instance, k, v)
        return instance


class Field:
    TYPE = object
    SCHEMA_TYPE = None

    def __init__(self, required=False):
        self.required = required

    def __set__(self, obj, value) -> None:
        if not isinstance(value, self.TYPE):
            raise ValueError('Not a {!r}: {!r}'.format(self.TYPE, value))

        self._value = value

    def __get__(self, obj, objtype=None):
        return self._value


class StringField(Field):
    TYPE = str
    SCHEMA_TYPE = 'string'


class IntegerField(Field):
    TYPE = int
    SCHEMA_TYPE = 'integer'


class FloatField(Field):
    TYPE = float
    SCHEMA_TYPE = 'number'
