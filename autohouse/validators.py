from django.core import validators, exceptions
import jsonschema


class CharacteristicJSONValidationSchema(validators.BaseValidator):

    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except Exception:
            raise exceptions.ValidationError(
                '%(value)s failed JSON schema check', params={'value': value}
            )
