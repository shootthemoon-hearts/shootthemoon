var socket;
var stream_to_event_handler_dict = {};
var multiplexed_event_handler= new value_is_key_event_handler("stream","payload");

function init_ws_connection() {
    socket = new WebSocket("ws://" + window.location.host);
    socket.onopen = init_game;
    socket.onmessage = rx_multiplexed_packet;
}

function tx_multiplexed_packet(stream,payload){
	var packet = {stream:stream,payload:payload};
	socket.send(JSON.stringify(packet));
}

function rx_multiplexed_packet(message){
	var packet = JSON.parse(message.data);
	multiplexed_event_handler.act_on(packet);
}

function bind_to_stream(stream, event_handler) {
	multiplexed_event_handler.register_handler(stream,event_handler);
}

