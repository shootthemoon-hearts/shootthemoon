/**
 * Creates the irresistible beautiful game board
 */

/**
 * Creates the graphics for the game to be synced up with the server which 
 * holds the game logic
 */
function createGame() {
    var board_length = 800;
    var board_height = 500;

    var card_length = 198;
    var card_height = 260;

    var player_cards = [];

	var game = new Phaser.Game(board_length, board_height, Phaser.AUTO, '', { preload: preload, create: create, update: update });

	/**
	 * Load images and such to be used in the game
	 */
	function preload() {

		game.load.spritesheet(Card.CLUBS, '../static/third_party/assets/card_images/clubs/different_playing_card_vector_graphic.jpg', card_length, card_height);
		game.load.spritesheet(Card.DIAMONDS, '../static/third_party/assets/card_images/diamonds/different_playing_card_vector_graphic.jpg', card_length, card_height);
		game.load.spritesheet(Card.HEARTS, '../static/third_party/assets/card_images/hearts/different_playing_card_vector_graphic.jpg', card_length, card_height);
		game.load.spritesheet(Card.SPADES, '../static/third_party/assets/card_images/spades/different_playing_card_vector_graphic.jpg', card_length, card_height);

        register_event_handler("Cards", got_cards);
	}
	
	/**
	 * Create the game
	 */
	function create () {
		//createFakeHand();
		//createMostDynamicGameBoardEver();
        //show_facedown_card();
        show_facedown_cards();


	}


	/**
	 * Update the game
	 */
	function update() {
		show_facedown_cards();
	}

    function got_cards(card_str) {
        console.log("got cards " + card_str);
        cards = Card.CardsFromJSON(card_str);
        player_cards = cards;
        update();
    }


    function show_facedown_cards() {
        total_hor_space_of_cards = 300;
        hor_start_x = board_length/2 - (total_hor_space_of_cards/2);
        hor_end_x = board_length/2 + (total_hor_space_of_cards/2 - 60);
        ver_start_x = board_height/2 - (total_hor_space_of_cards/2);
        ver_end_x = board_height/2 + (total_hor_space_of_cards/2 - 60);

        createHorizontalCards(50, hor_start_x, hor_end_x);
        createHorizontalCards(board_height - 50 - 130, hor_start_x, hor_end_x);
        createVerticalCards(50, ver_start_x, ver_end_x);
        createVerticalCards(board_length - 50 - 60, ver_start_x, ver_end_x);
    }

    function show_facedown_cards() {
        total_hor_space_of_cards = 300;
        hor_start_x = board_length/2 - (total_hor_space_of_cards/2);
        hor_end_x = board_length/2 + (total_hor_space_of_cards/2 - 60);
        ver_start_x = board_height/2 - (total_hor_space_of_cards/2);
        ver_end_x = board_height/2 + (total_hor_space_of_cards/2 - 60);

        createHorizontalCards([], 50, hor_start_x, hor_end_x);
        createHorizontalCards(player_cards, board_height - 50 - 130, hor_start_x, hor_end_x);
        createVerticalCards(50, ver_start_x, ver_end_x);
        createVerticalCards(board_length - 50 - 60, ver_start_x, ver_end_x);
    }

	/**
	 * This function is bad. Make it better. :)
	 */
	function createHorizontalCards(cards, y, start_x, end_x) {
        var use_fd = false;
        var len = cards.length;
        if (len == 0) {
            use_fd = true; 
            len = 13;
        } else {
            len = cards.length;
        }
		for (var i = 0; i < len; i++) {
			var x = ((end_x - start_x) / len * i) + start_x;

            var sprint = null;
            if (use_fd) {
			    sprite = create_facedown_card(game, x, y);
            } else {
                sprint = create_card_sprite(game, x, y, cards[i]);
            }
			// Also enable sprite for drag
			sprite.inputEnabled = true;
			sprite.input.enableDrag();
			sprite.events.onDragStart.add(startDrag, this);
			sprite.events.onDragStop.add(stopDrag, this);
		}
	}

	function createVerticalCards(x, start_y, end_y) {
        var len = 13;
		for (var i = 0; i < len; i++) {
			var y = ((end_y - start_y) / len * i) + start_y;

			var sprite = create_facedown_card(game, x, y);
			// Also enable sprite for drag
			sprite.inputEnabled = true;
			sprite.input.enableDrag();
			sprite.events.onDragStart.add(startDrag, this);
			sprite.events.onDragStop.add(stopDrag, this);
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
		socket.send('tileDragged');
	}
}
