import enum


class EnumSchemas(enum.Enum):
    CHARACTERISTIC_SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "brand": {"type": "string"},
            "model": {"type": "string"},
            "horse_power": {
                "type": "integer",
                "minimum": 1
            },
            "color": {"type": "string"},
            "year_of_issue": {
                "type": "integer",
                "minimum": 1800,
            },
            "transmission_type": {"type": "string"},
            "body-type": {"type": "string"},
            "price": {"type": "number"},
        },
    }
