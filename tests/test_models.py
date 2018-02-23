from unittest import TestCase

from jsonschema import ValidationError, validate

from jsom import models


class SimpleModel(models.Model):
    name = models.StringField(required=False)


class ModelTest(TestCase):
    def test_creates_simple_model(self):
        model = SimpleModel.create(
            name='Foo',
        )

        self.assertEqual(model.name, 'Foo')

    def test_cannot_create_with_inexisting_field(self):
        with self.assertRaises(AttributeError):
            SimpleModel.create(
                age=22,
            )

    def test_builds_schema_for_valid_data(self):
        schema_data = SimpleModel.as_schema()
        input_data = {
            'name': 'Foo',
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
            'name': 'Foo',
        })

        self.assertEqual(model.name, 'Foo')


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
