BEFORE_GAME = "BEFORE_GAME";
PASS_PHASE = "PASS_PHASE";
IN_TRICK = "IN_TRICK";



var game_board = null;
var player_cards = [];
var valid_cards = [];
var player_pos = null;
var selected_cards = [];
var my_turn = true;
var cards_to_select = 3;



var game_state = BEFORE_GAME;


function init_game() {

	game_event_handler.register_handler("Cards", got_cards);
	game_event_handler.register_handler("player_pos", got_player_pos);
	game_event_handler.register_handler("game_phase", new_game_phase);
	game_event_handler.register_handler("your_turn", now_my_turn);
	game_event_handler.register_handler("valid_cards", got_valid_cards);
	game_event_handler.register_handler("discard", got_discard);
	game_event_handler.register_handler("scores", got_scores);
	game_board = createGame();
};

function got_scores(score_list_dict){
	console.log(score_list_dict);
	destroy_discards_after_hand();
	score_textbox_p0.text = score_list_dict["score_list"][0];
	score_textbox_p1.text = score_list_dict["score_list"][1];
	score_textbox_p2.text = score_list_dict["score_list"][2];
	score_textbox_p3.text = score_list_dict["score_list"][3];
}

function got_discard(card_player_dict){
	//console.log(card_player_dict);
	createHorizontalDiscards(Card.CardsFromJSON(card_player_dict["card"])[0], card_player_dict["player"]);

}

function got_valid_cards(card_str){
	cards = Card.CardsFromJSON(card_str);
	valid_cards = cards;
}

function is_card_valid(card){
	for(var i = 0; i < valid_cards.length; i++){
		if(card.equals(valid_cards[i])){
			return true;
		}
	}
	return false;
}

function got_cards(card_str) {
    cards = Card.CardsFromJSON(card_str);
    player_cards = cards;
    show_facedown_cards(game_board, player_cards);
};

function got_player_pos(player) {
    player_pos = player;
};

function new_game_phase(phase) {
	game_state = phase;
	if (game_state == PASS_PHASE ){
		my_turn = true;
		cards_to_select = 3;
		selected_cards = [];
	}
	if (game_state == IN_TRICK) {
		my_turn = false;
		cards_to_select = 1;
		selected_cards = [];
	}
}

function now_my_turn(is_my_turn) {
	my_turn = is_my_turn;
}

function all_cards_selected() {
	var short_cards = [];
	for (card in selected_cards) {
		card = selected_cards[card];
		short_cards.push( card.toJSON());
	}
	my_turn = false;
	if (game_state == PASS_PHASE) {
		tx_multiplexed_packet("game",{'pass_cards_selected': short_cards});
	}
	if (game_state == IN_TRICK) {
		tx_multiplexed_packet("game",{'trick_card_selected': short_cards});
	}
}