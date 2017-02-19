from . import game_manager
from channels import Group
from . import event_manager
import json

def ws_add(message):
    '''Called when a websocket connection is made

    Args:
        message: The message sent by the client
    '''
    message.reply_channel.send({'accept':True})
    game_manager.player_connected(message.reply_channel)

def ws_disconnect(message):
    '''Called when a websocket connection is broken

    Args:
        message: The message sent by the client
    '''
    pass

def ws_message(message):
    '''Called when a client communicates via a websocket connection

    Args:
        message: The message sent by the client
    '''
    if 'text' in message.content:
        event = json.loads(message.content['text'])
        event_manager.event_received(event, message.reply_channel);
