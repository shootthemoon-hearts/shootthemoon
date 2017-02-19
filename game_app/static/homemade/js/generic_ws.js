socket = new WebSocket("ws://" + window.location.host + "/");
console.log("opening");

socket.onopen = function() {
    socket.send(JSON.stringify({
  		stream: "game",
  		payload: {"a":"b"}
	}));
	document.write("sending");
}

socket.onmessage = function(e) {
    document.write("got something");
}