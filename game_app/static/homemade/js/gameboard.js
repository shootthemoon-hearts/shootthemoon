/**
 * Creates the irresistible beautiful game board
 */

/**
 * Creates the graphics for the game to be synced up with the server which 
 * holds the game logic
 */
var board_length = 800;
var board_height = 500;

var card_length = 198;
var card_height = 260;


function show_facedown_cards(game_board, player_cards) {
    total_hor_space_of_cards = 300;
    hor_start_x = board_length/2 - (total_hor_space_of_cards/2);
    hor_end_x = board_length/2 + (total_hor_space_of_cards/2 - 60);
    ver_start_x = board_height/2 - (total_hor_space_of_cards/2);
    ver_end_x = board_height/2 + (total_hor_space_of_cards/2 - 60);

    createHorizontalCards([], 50, hor_start_x, hor_end_x, game_board);
    createHorizontalCards(player_cards, board_height - 50 - 130, hor_start_x, hor_end_x, game_board);
    createVerticalCards(50, ver_start_x, ver_end_x, game_board);
    createVerticalCards(board_length - 50 - 60, ver_start_x, ver_end_x, game_board);
}

/**
 * This function is bad. Make it better. :)
 */
function createHorizontalCards(cards, y, start_x, end_x, game_board) {
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
		    sprite = create_facedown_card(game_board, x, y);
        } else {
            sprite = create_card_sprite(game_board, x, y, cards[i]);
            sprite.card = cards[i];
            sprite.inputEnabled = true;
            sprite.clicked = false;
            sprite.events.onInputOver.add(mouseOn, game_board);
            sprite.events.onInputOut.add(mouseOff, game_board);
            sprite.events.onInputUp.add(cardClicked, game_board);
        }
	}
}

function createVerticalCards(x, start_y, end_y, game_board) {
    var len = 13;
	for (var i = 0; i < len; i++) {
		var y = ((end_y - start_y) / len * i) + start_y;

		var sprite = create_facedown_card(game_board, x, y);
	}
}

function mouseOn(sprite) {
	if (!sprite.clicked) {
		current_scale_x = sprite.scale.x;
		current_scale_y = sprite.scale.y;
		sprite.scale.set(current_scale_x * 1.1, current_scale_y * 1.1);
		sprite.tint = .8 * 0xFFFFFF;
	}
}

function mouseOff(sprite) {
	if (!sprite.clicked) {
		current_scale_x = sprite.scale.x;
		current_scale_y = sprite.scale.y;
		sprite.scale.set(current_scale_x / 1.1, current_scale_y / 1.1);
		sprite.tint = 0xFFFFFF;
	}
}

function cardClicked(sprite) {
	if (game_state != BEFORE_GAME) {
		if (!sprite.clicked) {
		
			sprite.tint = 0xFF0000;
			sprite.clicked = true;
			selected_cards.push(sprite.card);
			if (selected_cards.length == 3) {
				all_cards_selected();
			}
		}else {
			sprite.tint = 0xFFFFFF;
			sprite.clicked = false;
			selected_cards.remove(sprite.cards);
		} 
		
	}
}

function createGame() {

	var game = new Phaser.Game(board_length, board_height, Phaser.AUTO, '', { preload: preload, create: create, update: update });

	/**
	 * Load images and such to be used in the game
	 */
	function preload() {

		game.load.spritesheet(Card.CLUBS, '../static/third_party/assets/card_images/clubs/different_playing_card_vector_graphic.jpg', card_length, card_height);
		game.load.spritesheet(Card.DIAMONDS, '../static/third_party/assets/card_images/diamonds/different_playing_card_vector_graphic.jpg', card_length, card_height);
		game.load.spritesheet(Card.HEARTS, '../static/third_party/assets/card_images/hearts/different_playing_card_vector_graphic.jpg', card_length, card_height);
		game.load.spritesheet(Card.SPADES, '../static/third_party/assets/card_images/spades/different_playing_card_vector_graphic.jpg', card_length, card_height);

	}
	
	/**
	 * Create the game
	 */
	function create () {
        show_facedown_cards(this, player_cards);
	}

	/**
	 * Update the game
	 */
	function update() {

	}

	return game;
}