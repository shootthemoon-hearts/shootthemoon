from django.db import models  
from game_app.card import Card    
        
class CardListField(models.CharField):
    description = "Stores a list of Card objects as a concatenation of their \
    string values in the db"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 39 # 13 chars * 3 chars per card
        super(CardListField, self).__init__(*args, **kwargs)
        
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return Card.list_from_str(value)
    
    
    def to_python(self, value):
        if value is None:
            return None
        return Card.list_from_str(value)
    
    def get_prep_value(self, value):
        return Card.list_to_str(value)