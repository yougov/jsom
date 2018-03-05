from datetime import date, datetime
from enum import Enum


class ModelMeta(type):
    def __init__(cls, name, bases, attr_dict):
        for key, attr in attr_dict.items():
            if isinstance(attr, Field) and attr._name is None:
                attr._name = key


class Model:
    __metaclass__ = ModelMeta

    def __init__(self):
        self._values = {}

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
            schema_data['properties'][k] = v.as_property()

        return schema_data

    @classmethod
    def from_data(cls, data: dict):
        instance = cls()

        for k, v in data.items():
            field = cls.__dict__[k]
            decoded = field.decode(v)
            setattr(instance, k, decoded)

        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls()
        for k, v in kwargs.items():
            if k not in cls.__dict__:
                raise AttributeError('Invalid field: {}'.format(k))
            setattr(instance, k, v)
        return instance


class Sentinel(object):
    pass


class Field:
    TYPE = object
    SCHEMA_TYPE = None
    FORMAT = None

    def __init__(self, required=False, default=Sentinel):
        self.required = required
        self._value = None
        self._name = None
        self._default = default

    def __set__(self, obj: Model, value) -> None:
        type_ = self.get_type()
        if not isinstance(value, type_):
            raise ValueError('Not a {!r}: {!r}'.format(type_, value))

        self.validate(value)

        obj._values[self._name] = value

    def __get__(self, obj: Model, objtype=None):
        try:
            return obj._values[self._name]
        except KeyError:
            if self._default is not Sentinel:
                return self._default
            raise AttributeError('{} field has no value')

    def decode(self, value):
        return value

    def validate(self, value):
        pass

    def get_type(self):
        return self.TYPE

    def as_property(self):
        definition = {
            'type': self.SCHEMA_TYPE,
        }
        if self.FORMAT is not None:
            definition['format'] = self.FORMAT

        return definition


class StringField(Field):
    TYPE = str
    SCHEMA_TYPE = 'string'


class IntegerField(Field):
    TYPE = int
    SCHEMA_TYPE = 'integer'


class FloatField(Field):
    TYPE = float
    SCHEMA_TYPE = 'number'


class DateField(Field):
    TYPE = date
    SCHEMA_TYPE = 'string'
    FORMAT = 'date'

    def decode(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date()


class EnumField(Field):
    TYPE = Enum
    SCHEMA_TYPE = 'enum'

    def __init__(self, options: Enum, required=False):
        super().__init__(required=required)
        self.options = options

    def get_type(self):
        return self.options

    def as_property(self):
        return {
            'enum': list(self.options.__members__),
        }

    def decode(self, value):
        return self.options.__members__[value]
