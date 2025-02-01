from drf_spectacular.generators import SchemaGenerator,AutoSchema

class CustomSchemaGenerator(AutoSchema):

    def get_tags(self):
        tags = super().get_tags()
        if tags[0] == 'api':
            tags[0] = 'Accounts'
        return tags
