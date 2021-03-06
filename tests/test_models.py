import enum
from datetime import date
from unittest import TestCase

from jsonschema import ValidationError, validate

from jsom import models


class ModelMetaTest(TestCase):
    def test_empty_new(self):
        models.ModelMeta('ModelCls', (), {})

    def test_new_with_field(self):
        models.ModelMeta('ModelCls', (), dict(myfield=models.Field()))


class SimpleModel(models.Model):
    name = models.StringField(required=False)


class Fruits(enum.Enum):
    banana = 1
    apple = 2


class Colors(enum.Enum):
    red = 1
    blue = 2


class ModelTest(TestCase):
    def test_creates_simple_model(self):
        model = SimpleModel.create(
            name='Foo1',
        )

        self.assertEqual(model.name, 'Foo1')

    def test_cannot_create_with_inexisting_field(self):
        with self.assertRaises(AttributeError):
            SimpleModel.create(
                age=22,
            )

    def test_builds_schema_for_valid_data(self):
        schema_data = SimpleModel.as_schema()
        input_data = {
            'name': 'Foo2',
        }

        validate(input_data, schema_data)

    def test_builds_flexible_schema(self):
        schema_data = SimpleModel.as_schema()
        input_data = {
            'age': 22,
        }

        validate(input_data, schema_data)

    def test_builds_restrictive_schema(self):
        class SimpleModel(models.Model):
            name = models.StringField(required=True)

        schema_data = SimpleModel.as_schema()
        input_data = {
            'age': 22,
        }

        with self.assertRaises(ValidationError):
            validate(input_data, schema_data)

    def test_builds_a_model_instance_from_valid_data(self):
        model = SimpleModel.from_data({
            'name': 'Foo3',
        })

        self.assertEqual(model.name, 'Foo3')


class FieldTest(TestCase):
    def test_does_not_interfere_with_class_attributes(self):
        SimpleModel.create(name='Foo')
        model = SimpleModel()

        with self.assertRaises(AttributeError):
            model.name

    def test_uses_default_value_if_needed(self):
        class EmptyModel(models.Model):
            something = models.Field(default='my-default')

        model = EmptyModel()

        self.assertEqual(model.something, 'my-default')

    def test_accepts_none_as_default(self):
        class EmptyModel(models.Model):
            something = models.Field(default=None)

        model = EmptyModel()

        self.assertIsNone(model.something)


class StringFieldTest(TestCase):
    def test_accepts_string(self):
        model = SimpleModel()

        model.name = 'Foo'

        self.assertEqual(model.name, 'Foo')

    def test_doesnt_accept_integer(self):
        model = SimpleModel()

        with self.assertRaises(ValueError):
            model.name = 22


class IntegerFieldTest(TestCase):
    class SomeModel(models.Model):
        age = models.IntegerField()

    def test_accepts_integer(self):
        model = self.SomeModel()
        model.age = 22

        self.assertEqual(model.age, 22)

    def test_doesnt_accept_string(self):
        model = self.SomeModel()

        with self.assertRaises(ValueError):
            model.age = 'twenty-two'

    def test_is_referenced_in_schema_as_integer(self):
        schema_data = self.SomeModel.as_schema()
        input_data = {
            'age': 22,
        }

        validate(input_data, schema_data)

    def test_translates_data_to_internal_type(self):
        model = self.SomeModel.from_data({
            'age': 22,
        })

        self.assertEqual(model.age, 22)


class FloatFieldTest(TestCase):
    class SomeModel(models.Model):
        height = models.FloatField()

    def test_accepts_float(self):
        model = self.SomeModel()
        model.height = 1.77

        self.assertEqual(model.height, 1.77)

    def test_doesnt_accept_string(self):
        model = self.SomeModel()

        with self.assertRaises(ValueError):
            model.height = 'very tall'

    def test_is_referenced_in_schema_as_number(self):
        schema_data = self.SomeModel.as_schema()
        input_data = {
            'height': 1.77,
        }

        validate(input_data, schema_data)

    def test_translates_data_to_internal_type(self):
        model = self.SomeModel.from_data({
            'height': 1.77,
        })

        self.assertEqual(model.height, 1.77)


class DateFieldTest(TestCase):
    class SomeModel(models.Model):
        when = models.DateField()

    def test_accepts_date(self):
        model = self.SomeModel()
        model.when = date(2018, 1, 1)

        self.assertEqual(model.when, date(2018, 1, 1))

    def test_doesnt_accept_string(self):
        model = self.SomeModel()

        with self.assertRaises(ValueError):
            model.when = 'very late'

    def test_is_referenced_in_schema_as_date(self):
        schema_data = self.SomeModel.as_schema()
        input_data = {
            'when': '2018-01-01',
        }

        validate(input_data, schema_data)

    def test_translates_data_to_internal_type(self):
        model = self.SomeModel.from_data({
            'when': '2018-01-01',
        })

        self.assertEqual(model.when, date(2018, 1, 1))


class EnumFieldTest(TestCase):
    class SomeModel(models.Model):
        fruit = models.EnumField(options=Fruits)

    def test_accepts_local_enum(self):
        model = self.SomeModel()
        model.fruit = Fruits.banana

        self.assertEqual(model.fruit, Fruits.banana)

    def test_doesnt_accept_string(self):
        model = self.SomeModel()

        with self.assertRaises(ValueError):
            model.fruit = 'passion fruit'

    def test_doesnt_accept_another_enum(self):
        model = self.SomeModel()

        with self.assertRaises(ValueError):
            model.fruit = Colors.red

    def test_is_referenced_in_schema_as_enum(self):
        schema_data = self.SomeModel.as_schema()
        input_data = {
            'fruit': 'banana',
        }

        validate(input_data, schema_data)

    def test_translates_data_to_internal_type(self):
        model = self.SomeModel.from_data({
            'fruit': 'banana',
        })

        self.assertEqual(model.fruit, Fruits.banana)
