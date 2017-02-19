event_handler_dict = {};

def register_event_handler(key, handler):
    event_handler_dict[key] = handler
     
def event_received(event, channel):
    for key, value in event.items():
        if key in event_handler_dict:
            event_handler_dict[key](value, channel)