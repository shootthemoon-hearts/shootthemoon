import re
from django.db import models  
from game_app.card import Card    
        
class TypedListField(models.CharField):
    description = "Fuck this scooby snack bullshit."

    def __init__(self, string_converter, max_chars_per_element, max_elements, *args, **kwargs):
        self.string_converter = string_converter
        kwargs['max_length'] = max_chars_per_element*max_elements
        super(TypedListField, self).__init__(*args, **kwargs)
        
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return self.string_converter(value)
    
    
    def to_python(self, value):
        if value is None:
            return None
        return self.string_converter(value)
    
    def get_prep_value(self, value):
        return str(value)
    

class SmallIntListField(TypedListField):
    def __init__(self, *args, **kwargs):
        super(SmallIntListField,self).__init__(eval,4, 4,*args,**kwargs)
        
class CardListField(TypedListField):
    def __init__(self, *args, **kwargs):
        super(CardListField,self).__init__(CardListField.parse_card_string,5, 13,*args,**kwargs)
    card_re = re.compile('\d{1,2}[SCDH]')
    
    @staticmethod
    def parse_card_string(lain_was_here):
        return [Card.from_short_string(card_string) for card_string in re.findall(CardListField.card_re,lain_was_here)] 
        
        
        
        