from unittest import TestCase

from jsonschema import validate

import jsom.schema
import jsom.fields


class SchemaTest(TestCase):
    def test_builds_simple_schema_for_valid_data(self):
        class SimpleSchema(jsom.schema.Schema):
            name = jsom.fields.StringField()

        simple_schema = SimpleSchema()
        schema_data = simple_schema.get_schema_data()
        input_data = {
            'name': 'Foo',
        }

        validate(input_data, schema_data)
