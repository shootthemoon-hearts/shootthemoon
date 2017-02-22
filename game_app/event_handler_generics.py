class generic_event_handler:
    key_to_handler_dict = {}
    def register_handler(self,key,handler):
        self.key_to_handler_dict[key] = handler;

class value_is_key_event_handler(generic_event_handler):
    def __init__(self,key_key,payload_key):
        self.key_key = key_key
        self.payload_key = payload_key
    def act_on (self,data_dict,*args):
        key = data_dict[self.key_key]
        payload = data_dict[self.payload_key]
        if key in self.key_to_handler_dict:
            handler = self.key_to_handler_dict[key]
            handler(payload,*args);

class key_is_key_event_handler(generic_event_handler):
    def act_on (self,data_dict,*args):
        for key in data_dict:
            if key in self.key_to_handler_dict:
                payload = data_dict[key]
                handler = self.key_to_handler_dict[key]
                handler(payload,*args);




