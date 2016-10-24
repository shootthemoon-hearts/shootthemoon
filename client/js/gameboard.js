/**
 * Creates the irresistible beautiful game board
 */

/**
 * Creates the graphics for the game to be synced up with the server which 
 * holds the game logic
 */
function createGame() {
	var game = new Phaser.Game(800, 600, Phaser.AUTO, '', { preload: preload, create: create, update: update });

	/**
	 * Load images and such to be used in the game
	 */
	function preload() {
		game.load.image('tile', '../third_party/assets/mahjong-icon.png');
	}
	
	/**
	 * Create the game
	 */
	function create () {
		createFakeHand();
		createMostDynamicGameBoardEver();
	}

	/**
	 * Update the game
	 */
	function update() {
		
	}

	/**
	 * Creates a fake hand for a player. Needs some work...
	 */
	function createFakeHand() {
		var hands = [];
		var num_players = 4;
		var num_tiles = 13;
		for (var i = 0; i < num_players; i++) {
			var tiles = []
			for (var tile_idx = 0; tile_idx < num_tiles; tile_idx++){
				var value = Math.floor(Math.random() * (9 - 0)) + 0;
				var suit = "sou";
				tiles[tile_idx] = new Tile(suit, value);
			}

			hands[i] = new Hand(tiles);
		}

		var hand_str = '';
		for (i = 0; i < num_tiles; i++) {
			hand_str += hands[0].tiles[i].value;
		}
	}

	/**
	 * Creates the most dynamic and beautiful game board that you've ever seen
	 * in the history of Anime
	 */
	function createMostDynamicGameBoardEver() {

		var array = (function() {
			var array = [];
			for (var i = 0; i < 13; i++) {
				array.push('tile');
			}
			return array;
		})();
		fillHorizontalText(array, 50, 50, 400);
		fillHorizontalText(array, 375, 50, 400);

		fillVerticalText(array, 10, 70, 380);
		fillVerticalText(array, 410, 70, 380);
	}

	/**
	 * This function is bad. Make it better. :)
	 */
	function fillHorizontalText(text, y, start_x, end_x) {
		text = Array.from(text);
		for (var i = 0; i < text.length; i++) {
			var x = ((end_x - start_x) / text.length * i) + start_x;

			var sprite = game.add.sprite(x, y, text[i]);
			// Also enable sprite for drag
			sprite.inputEnabled = true;
			sprite.input.enableDrag();
			sprite.events.onDragStart.add(startDrag, this);
			sprite.events.onDragStop.add(stopDrag, this);
		}
	}

	/**
	 * This function is also bad. Make it betterer. :)
	 */
	function fillVerticalText(text, x, start_y, end_y) {
		text = Array.from(text);
		for (var i = 0; i < text.length; i++) {
			var y = ((end_y - start_y) / text.length * i) + start_y;

			var sprite = game.add.sprite(x, y, text[i]);
			// Also enable sprite for drag
			sprite.inputEnabled = true;
			sprite.input.enableDrag();
			sprite.events.onDragStart.add(startDrag, this);
			sprite.events.onDragStop.add(stopDrag, this);
		}
	}

	/**
	 * Called when the player begins to drag a tile
	 */
	function startDrag() {
		console.log("Drag Started");
	}

	/**
	 * Called when the player finishes dragging a tile
	 */
	function stopDrag(sprite) {
		console.log("Drag Stopped");
		IO.socket.emit('tileDragged', {'a': 'b'});
	}
}