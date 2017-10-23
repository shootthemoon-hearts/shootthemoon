from django.db import models

class EnumField(models.IntegerField):
    #TODO: Update description
    description = "Store int-based enums in the database without having to convert to and from an int each time."

    def __init__(self, enum_class=None, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        self.enum_class = enum_class

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return self.enum_class(value)

    def to_python(self, value):
        if value is None:
            return None
        return self.enum_class(value)

    def get_prep_value(self, value):
        return value.value
