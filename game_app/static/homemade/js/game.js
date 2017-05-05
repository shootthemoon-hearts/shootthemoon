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
	game_event_handler.register_handler("trick", trick_update);
	game_event_handler.register_handler("valid_cards", got_valid_cards);
	game_event_handler.register_handler("discard", got_discard);
	game_event_handler.register_handler("scores", got_scores);
}

function init_game(game_info_dict) {
	player_pos = game_info_dict['player_pos'];
	game_board = createGame();
}

function relative_seat(seat,base_seat){
	return (seat-base_seat+4)%4;
}

function got_scores(score_list_dict){
	//destroy_discards_after_hand();
	score_textbox_p0.text = score_list_dict["score_list"][0];
	score_textbox_p1.text = score_list_dict["score_list"][1];
	score_textbox_p2.text = score_list_dict["score_list"][2];
	score_textbox_p3.text = score_list_dict["score_list"][3];
}

function got_discard(card_player_dict){
	var trick_id = card_player_dict["id"];
	var relative_player_seat = relative_seat(card_player_dict["player"],player_pos);
	var card = Card.CardsFromJSON(card_player_dict["card"])[0];
	var discard_pile = trick_group.getByName(trick_id.toString());
	hand_group.children[relative_player_seat].passToCardGroup([card],discard_pile);
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
		//my_turn = false;
		cards_to_select = 1;
		selected_cards = [];
	}
}

function trick_update(trick_dict) {
	var trick_id = trick_dict['id'];
	var relative_player_seat = relative_seat(trick_dict["player"],player_pos);
	if (trick_group.countLiving() > 1){
		var to_die = trick_group.countLiving() -1;
		for (var i=0; i<to_die; i++){
			trick_group.children[i].alive = false;
		}
	}
	trick_group.forEachDead(trick_group.remove, trick_group, true, true);
	if (trick_group.getByName(trick_id.toString()) == undefined){
		var location = new Phaser.Point(300,200);
		var scale_factor = new Phaser.Point(0.7,0.7);
		var pile = trick_group.addChild(new DiscardPile(game_board,relative_player_seat,100,5,8,15));
		pile.name = trick_id.toString();
		location.copyTo(pile.position);
		scale_factor.copyTo(pile.scale);
	}
	if (relative_player_seat ==0){
		turn_id = trick_id;
		my_turn = true;
	}else{
		my_turn = false;
	}
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