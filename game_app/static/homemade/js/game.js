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
var turn_id = 0;
var hand_group = null;
var trick_group = null;




var game_state = BEFORE_GAME;

function register_handlers() {
	game_event_handler.register_handler("enter_room", init_game);
	game_event_handler.register_handler("Cards", got_cards);
	game_event_handler.register_handler("game_phase", new_game_phase);
	game_event_handler.register_handler("your_turn", now_my_turn);
	game_event_handler.register_handler("valid_cards", got_valid_cards);
	game_event_handler.register_handler("discard", got_discard);
	game_event_handler.register_handler("scores", got_scores);
}

function init_game(game_info_dict) {
	player_pos = game_info_dict['player_pos'];
	game_board = createGame();
}

function got_scores(score_list_dict){
	//destroy_discards_after_hand();
	score_textbox_p0.text = score_list_dict["score_list"][0];
	score_textbox_p1.text = score_list_dict["score_list"][1];
	score_textbox_p2.text = score_list_dict["score_list"][2];
	score_textbox_p3.text = score_list_dict["score_list"][3];
}

function got_discard(card_player_dict){
	var card = Card.CardsFromJSON(card_player_dict["card"])[0];
	var relative_player_seat = (card_player_dict["player"]-player_pos+4)%4;
	var hand_length = card_player_dict["remaining"];
	
	hand_group.children[relative_player_seat].passToCardGroup([card],trick_group.children[0]);
	//if(relative_player_seat!=0 && hand_group!=null){
	//	hand_group.children[relative_player_seat].fillWithFaceDowns(hand_length,500);
	//}
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
    hand_group.children[0].updateCardState(player_cards,500);
    if (cards.length == 13){
    	hand_group.children[1].fillWithFaceDowns(13,500);
    	hand_group.children[2].fillWithFaceDowns(13,500);
    	hand_group.children[3].fillWithFaceDowns(13,500);
    }
    
}

function new_game_phase(phase) {
	game_state = phase;
	if (game_state == PASS_PHASE ){
		my_turn = false;
		cards_to_select = 3;
		selected_cards = [];
	}
	if (game_state == IN_TRICK) {
		my_turn = false;
		cards_to_select = 1;
		selected_cards = [];
		if (trick_group.children.length>0){
			trick_group.children[0].dematerializeTowards(0);
		}
		var pile = trick_group.addChild(new DiscardPile(game_board,0,100,20,5,30));
		pile.x = 300; pile.y = 200;
	}
}

function now_my_turn(my_turn_id) {
	turn_id = my_turn_id;
	my_turn = true;
}

function all_cards_selected() {
	var short_cards = [];
	for (card in selected_cards) {
		card = selected_cards[card];
		short_cards.push( card.toJSON());
	}
	my_turn = false;
	if (game_state == PASS_PHASE) {
		tx_multiplexed_packet("game",{'pass_cards_selected': {'received_cards':short_cards, 'turn_id':turn_id}});
	}
	if (game_state == IN_TRICK) {
		tx_multiplexed_packet("game",{'trick_card_selected': {'received_cards':short_cards, 'turn_id':turn_id}});
	}
}