var GameState = function(){
	BEFORE_GAME = "BEFORE_GAME";
	PASS_PHASE = "PASS_PHASE";
	IN_TRICK = "IN_TRICK";

	this.game_board = null;
	this.player_cards = [];
	this.valid_cards = [];
	this.player_pos = null;
	this.selected_cards = [];
	this.my_turn = true;
	this.cards_to_select = 3;
	this.turn_id = 0;
	this.hand_group = null;
	this.trick_group = null;
	this.myTimer = null;
	this.phase = BEFORE_GAME;
	
    this.score_textbox_p0 = null;
    this.score_textbox_p1 = null;
    this.score_textbox_p2 = null;
    this.score_textbox_p3 = null;
}