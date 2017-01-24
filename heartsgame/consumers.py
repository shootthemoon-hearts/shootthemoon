from . import game_manager
from channels import Group

def ws_add(message):
    message.reply_channel.send({'accept':True})
    game_manager.player_connected(message.reply_channel)

# Connected to websocket.disconnet
def ws_disconnect(message):
    pass

def ws_message(message):
    if 'text' in message.content:
        print(message.content['text'])
