var socket;
var stream_to_event_handler_dict = {};

function init_ws_connection() {
    socket = new WebSocket("ws://" + window.location.host);
    socket.onmessage = rx_multiplexed_packet;
}


function tx_multiplexed_packet(stream,payload){
	var packet = {stream:stream,payload:payload};
	socket.send(JSON.stringify(packet));
}

function rx_multiplexed_packet(message){
	var packet = JSON.parse(message.data);
	var stream = packet['stream'];
	var payload = packet['payload'];
	if (stream_to_event_handler_dict.hasOwnProperty(stream)) {
		var handler = stream_to_event_handler_dict[stream];
		handler(payload);
	}
}

function bind_to_stream(stream, event_handler) {
	stream_to_event_handler_dict[stream] = event_handler;
}

