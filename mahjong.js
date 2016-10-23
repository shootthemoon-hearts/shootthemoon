'use strict';
var io;
var gameSocket;

/**
 * This function is called by index.js to initialize a new game instance.
 *
 * @param sio The Socket.IO library
 * @param socket The socket object for the connected client.
 */

var MahjonggGame = function (sio, socket) {
	this.io = sio;
	this.gameSocket = socket;
	this.sessionId = Math.random();
	this.players = 0

	// Host Events
	this.io.sockets.on('tileDragged', tileDragged);
//    gameSocket.on('hostRoomFull', hostPrepareGame);
//    gameSocket.on('hostCountdownFinished', hostStartGame);
//    gameSocket.on('hostNextRound', hostNextRound);
//
//    // Player Events
	this.io.sockets.on('playerJoinGame', this.playerJoinGame);
//    gameSocket.on('playerAnswer', playerAnswer);
//    gameSocket.on('playerRestart', playerRestart);

};
exports.MahjonggGame = MahjonggGame;
	
MahjonggGame.prototype.playerJoinGame = function (socket) {
	console.log("Player connected");
	socket.emit('connected', this.sessionId);
	this.players += 1;
	console.log(this.players);
	
}

function tileDragged(data) {
	console.log("got drag event");
	console.log(data);
}