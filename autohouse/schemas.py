import enum


class EnumSchemas(enum.Enum):
    CHARACTERISTIC_SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "brand": {"type": "string"},
            "color": {"type": "string"},
            "year_of_issue": {
                "type": "string",
                "format": "date"
            },
            "type_of_transmission": {"type": "string"}
        },
    }
