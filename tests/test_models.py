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

    def test_builds_schema_for_integer_data(self):
        class SomeModel(models.Model):
            age = models.IntegerField()

        schema_data = SomeModel.as_schema()
        input_data = {
            'age': 22,
        }

        validate(input_data, schema_data)

    def test_builds_schema_for_float_data(self):
        class SomeModel(models.Model):
            height = models.FloatField()

        schema_data = SomeModel.as_schema()
        input_data = {
            'height': 1.77,
        }

        validate(input_data, schema_data)


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
    def test_accepts_integer(self):
        class SomeModel(models.Model):
            age = models.IntegerField()

        model = SomeModel()
        model.age = 22

        self.assertEqual(model.age, 22)

    def test_doesnt_accept_string(self):
        class SomeModel(models.Model):
            age = models.IntegerField()

        model = SomeModel()

        with self.assertRaises(ValueError):
            model.age = 'twenty-two'


class FloatFieldTest(TestCase):
    def test_accepts_float(self):
        class SomeModel(models.Model):
            height = models.FloatField()

        model = SomeModel()
        model.height = 1.77

        self.assertEqual(model.height, 1.77)

    def test_doesnt_accept_string(self):
        class SomeModel(models.Model):
            height = models.FloatField()

        model = SomeModel()

        with self.assertRaises(ValueError):
            model.height = 'very tall'
