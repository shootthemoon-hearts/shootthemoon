// Import the Express module
var express = require('express');

// Import the 'path' module (packaged with Node.js)
var path = require('path');

// Create a new instance of Express
var app = express();

// Import the mahjong game file.
var mahjong = require('./mahjong');

// Serve static html, js, css, and image files from the 'client' directory
app.use(express.static(path.join(__dirname,'client')));

// Create a Node.js based http server on port 8080
var server = require('http').createServer(app).listen(process.env.PORT || 8080);

// Create a Socket.IO server and attach it to the http server
var io = require('socket.io').listen(server);

// Listen for Socket.IO Connections. Once connected, start the game logic.
var game = null;
io.sockets.on('connection', function (socket) {
	if (game == null || game.players % 4 == 0) {
		game = new mahjong.MahjonggGame(io, socket);
	}
	game.playerJoinGame(socket);
});