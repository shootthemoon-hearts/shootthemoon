/**
 * Creates the graphics for the game to be synced up with the server which holds
 * the game logic
 */

CARD_SPRITE_SHEET = 'cards';

var board_length = 800;
var board_height = 600;

var card_length = 146;
var card_height = 195.5;

var score_textbox = null;

var my_location_x = (board_length/2) - 10;
var my_location_y = (board_height/1.13);

var left_location_x = (board_length/50);
var left_location_y = (board_height/2);

var across_location_x = (board_length/2) - 10;
var across_location_y = (board_height/30);

var right_location_x = (board_length/1.04);
var right_location_y = (board_height/2);

var game_board_functions = {
	createDiscardPile: function(game_state, trick_id) {
		var location = new Phaser.Point(300,200);
		var scale_factor = new Phaser.Point(0.7,0.7);
		var pile = new DiscardPile(game_state.game_controller, game_state.relative_player_seat, 100, 5, 8, 15);
		pile.name = trick_id.toString();
		location.copyTo(pile.position);
		scale_factor.copyTo(pile.scale);
		return pile;
	},

	createPlayerIcons: function(phaser_game, player_pos) {
		// TODO(Matt Weiss) Replace with players' usernames
        if(player_pos == 0){
        	p0 = phaser_game.add.text(my_location_x, my_location_y,"p0");
    		p1 = phaser_game.add.text(left_location_x, left_location_y,"p1");
    		p2 = phaser_game.add.text(across_location_x, across_location_y,"p2");
    		p3 = phaser_game.add.text(right_location_x, right_location_y,"p3");
        } else if(player_pos == 1){
        	p1 = phaser_game.add.text(my_location_x, my_location_y,"p1");
    		p2 = phaser_game.add.text(left_location_x, left_location_y,"p2");
    		p3 = phaser_game.add.text(across_location_x, across_location_y,"p3");
    		p0 = phaser_game.add.text(right_location_x, right_location_y,"p0");
        } else if(player_pos == 2){
        	p2 = phaser_game.add.text(my_location_x, my_location_y,"p2");
    		p3 = phaser_game.add.text(left_location_x, left_location_y,"p3");
    		p0 = phaser_game.add.text(across_location_x, across_location_y,"p0");
    		p1 = phaser_game.add.text(right_location_x, right_location_y,"p1");
        } else if(player_pos == 3){
        	p3 = phaser_game.add.text(my_location_x, my_location_y,"p3");
    		p0 = phaser_game.add.text(left_location_x, left_location_y,"p0");
    		p1 = phaser_game.add.text(across_location_x, across_location_y,"p1");
    		p2 = phaser_game.add.text(right_location_x, right_location_y,"p2");
        }
		p0.fill = "blue";
        p1.fill = "red";
        p2.fill = "green";
        p3.fill = "yellow";
	}
}

function create_turn_indicator(game, x, y, image) {
	sprite = game.add.sprite(x, y, image);
}

function createGame(game_controller) {

	var phaser_game = new Phaser.Game(board_length, board_height, Phaser.AUTO, 'game_board', { preload: preload, create: create, update: update });

	/**
	 * Load images and such to be used in the game
	 */
	function preload() {

		phaser_game.load.spritesheet(Card.BACK, '../static/third_party/assets/card_images/card_back.png', card_length, card_height);
		phaser_game.load.spritesheet(CARD_SPRITE_SHEET, '../static/third_party/assets/card_images/card_sheet.png', card_length, card_height, 52);
		
		phaser_game.load.image("turn_no", "../static/homemade/assets/turn_no.png");
		phaser_game.load.image("turn_yes", "../static/homemade/assets/turn_yes.png");
		
		phaser_game.load.image("background", "../static/homemade/assets/table_bg.png");
	}
	
	/**
	 * Create the game board
	 */
	function create () {
		var game_state = game_controller.game_state;
		game_state.game_board = phaser_game;
		
		background = phaser_game.add.tileSprite(0, 0, 800, 600, "background");

		game_state.hand_group = phaser_game.add.group();
		game_state.hand_group.addChild(new Hand(game_controller,20,50,0)).position = new Phaser.Point(my_location_x,my_location_y-210);
		game_state.hand_group.addChild(new Hand(game_controller,20,50,1)).position = new Phaser.Point(left_location_x+210,left_location_y);
		game_state.hand_group.addChild(new Hand(game_controller,20,50,2)).position = new Phaser.Point(across_location_x,across_location_y+210);
		game_state.hand_group.addChild(new Hand(game_controller,20,50,3)).position = new Phaser.Point(right_location_x-210,right_location_y);
		
		var scale_factor = new Phaser.Point(0.7,0.7);
		game_state.hand_group.children[0].angle =   0;
		game_state.hand_group.children[1].angle =  90;
		game_state.hand_group.children[2].angle = 180;
		game_state.hand_group.children[3].angle = 270;
		scale_factor.copyTo(game_state.hand_group.children[0].scale);
		scale_factor.copyTo(game_state.hand_group.children[1].scale);
		scale_factor.copyTo(game_state.hand_group.children[2].scale);
		scale_factor.copyTo(game_state.hand_group.children[3].scale);
		
		game_state.trick_group = phaser_game.add.group();

		game_state.myTimer = new Timer(phaser_game, game_state);
		phaser_game.stage.addChild(game_state.myTimer.textDisplay);

		
		/// creating the not someone's turn indicators at near-player-card locations  ///
		create_turn_indicator(phaser_game, my_location_x + 33, my_location_y,"turn_no");
		create_turn_indicator(phaser_game, left_location_x, left_location_y + 30,"turn_no");
		create_turn_indicator(phaser_game, across_location_x + 30, across_location_y,"turn_no");
		create_turn_indicator(phaser_game, right_location_x, right_location_y + 30,"turn_no");
		
        //show_facedown_cards(this, player_cards);
        ///super terrible lazy code, going to be deleted anyways later cus temporary///
        game_state.score_textbox_p0 = phaser_game.add.text((board_length/1.25), (board_height/7), "0");
        game_state.score_textbox_p0.fill = "blue";
        game_state.score_textbox_p1 = phaser_game.add.text((board_length/1.25) + 40, (board_height/7), "0");
        game_state.score_textbox_p1.fill = "red";
        game_state.score_textbox_p2 = phaser_game.add.text((board_length/1.25) + 80, (board_height/7), "0");
        game_state.score_textbox_p2.fill = "green";
        game_state.score_textbox_p3 = phaser_game.add.text((board_length/1.25) + 120, (board_height/7), "0");
        game_state.score_textbox_p3.fill = "yellow";
	}
	
	/**
	 * Update the gameboard
	 */
	function update() {

	}

	return phaser_game;
}