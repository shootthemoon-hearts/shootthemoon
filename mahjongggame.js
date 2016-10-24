/**
 * This file manages all of the game logic for a single game. It manages
 * communication with the clients. When it receives messages from the clients,
 * it updates the game logic appropriately and then informs all clients of the
 * next state.
 */
'use strict';

/**
 * Constructor for the MahjonggGame class
 *
 * @param io The Socket.IO instance responsible for managing connections
 * between server and client instances
 * @param id The id associated with the game
 */
var MahjonggGame = function (io, id) {
	this.io = io;
	this.players = 0;
	this.gameID = id;
};

// Export this so it can be used from other scripts
exports.MahjonggGame = MahjonggGame;

/**
 * Returns whether or not the room is full
 *
 * @returns whether or not the room is full
 */
MahjonggGame.prototype.isFull = function () {
	return this.players >= 4;
}


/**
 * Adds a player to the game. Also sends out an event to the added player
 * letting them know they have been successfully added and the room they have 
 * been added to.
 * 
 * @param socket The socket that can be used to communicate with the player
 */
MahjonggGame.prototype.addPlayer = function (socket) {
	socket.emit('connected', this.gameID);
	this.players += 1;
	console.log(this.players);
}

/**
 * This function is called when a client drags a tile. This should get replaced
 * later with real game events made by the players. 
 * 
 * @param data data regarding the tile that was dragged; currently nothing 
 * useful.
 */
function tileDragged(data) {
	console.log("got drag event");
	console.log(data);
}