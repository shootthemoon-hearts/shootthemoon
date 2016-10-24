/**
 * File responsible for managing game rooms and assigning players to games.
 */

// Import the MahjonggGame class.
var MahjonggGame = require('./mahjongggame').MahjonggGame;

var io = null;
/**
 * This function starts the game manager. The game manager is responsible for:
 * 1) Creating games
 * 2) Adding players to games
 * 
 * @param io The Socket.IO instance responsible for managing connections
 * 		between server and client instances
 */
exports.start = function(io) {
	// The following logic is basic logic that will place incoming players into 
	// rooms. When anyone connects to the game server (simply going to the 
	// appropriate URL), the following function is
	// automatically called (the client will send a 'connection' event). Then, it
	// will check to see if any of the rooms have room for additional players. If
	// yes, it will place the player into an existing room, otherwise, it will 
	// create a new room.
	var games = [];
	io.sockets.on('connection', function (socket) {
		var game = null;
		
		// If no games have been created, create one
		if (games.length == 0) {
			game = new MahjonggGame(io, 1);
			games.push(game);

		} else {

			// Check if any of the existing rooms aren't full
			var found_game = false;
			for (index = 0; index < games.length; index++) {
				if (!games[index].isFull()) {
					game = games[index];
					found_game = true;
					break;
				}
			}
			
			// They're all full, create a new game
			if (!found_game) {
				game = new MahjonggGame(io, games.length + 1);
				games.push(game);
			}

		}
		game.addPlayer(socket);
	});
};