from channels.auth import channel_session_user, channel_session_user_from_http

@channel_session_user_from_http
def ws_add(message):
    '''Called when a websocket connection is made

    Args:
        message: The message sent by the client
    '''
    message.reply_channel.send({'accept':True})

@channel_session_user
def ws_disconnect(message):
    '''Called when a websocket connection is broken

    Args:
        message: The message sent by the client
    '''
    pass

