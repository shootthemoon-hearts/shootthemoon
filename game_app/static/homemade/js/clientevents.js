/**
 * This file sends updates to the server when 
 * the player makes a move, and receives new states from the server.
 * 
 * This is called when the page is displayed. It connects the Socket.IO 
 * client to the Socket.IO server
 */

var game_event_handler = new key_is_key_event_handler();
bind_to_stream("game", game_event_handler.act_on)
init_ws_connection();
register_handlers();