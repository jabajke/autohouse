import enum


class EnumSchemas(enum.Enum):
    CHARACTERISTIC_SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "brand": {"type": "string"},
            "model": {"type": "string"},
            "horse_power": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "integer",
                        "minimum": 1
                    },
                    "actions": {
                        "default": "in",
                        "enum": ["gt", "gte", "lt", "lte", "eq"]
                    },
                },
                "required": ["value", "actions"]
            },
            "color": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True
            },
            "year_of_issue": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "integer",
                        "minimum": 1800
                    },
                    "actions": {
                        "enum": ["gt", "gte", "lt", "lte", "eq"]
                    },
                },
                "required": ["value", "actions"]
            },
            "transmission_type": {"enum": ["manual", "automatic", "cvt"]},
            "body_type": {"enum":
                [
                    "sedan",
                    "coupe",
                    "hatchback",
                    "minivan",
                    "pickup"
                ]
            },
        },
    }
