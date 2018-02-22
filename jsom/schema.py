class Schema:
    def get_schema_data(self):
        schema_data = {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                },
            },
        }

        return schema_data
