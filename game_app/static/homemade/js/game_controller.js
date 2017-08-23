var GameController = function(){
	this.game_state = new GameState();
	this.game_event_handler = null;
}

GameController.prototype.register_handlers = function(game_event_handler) {
	this.game_event_handler = game_event_handler;
	game_event_handler.register_handler("enter_room", this.init_game, this);
	game_event_handler.register_handler("Cards", this.got_cards, this);
	game_event_handler.register_handler("game_phase", this.new_game_phase, this);
	game_event_handler.register_handler("trick", this.trick_update, this);
	game_event_handler.register_handler("valid_cards", this.got_valid_cards, this);
	game_event_handler.register_handler("discard", this.got_discard, this);
	game_event_handler.register_handler("scores", this.got_scores, this);
}

GameController.prototype.init_game = function(game_info_dict) {
	this.game_state.player_pos = game_info_dict['player_pos'];
	this.game_state.game_board = createGame(this.game_state);
}

GameController.prototype.get_relative_seat = function(seat,base_seat){
	return (seat-base_seat+4)%4;
}

GameController.prototype.got_time_info = function(time_list){
	start_time = time_list[0];
	base_time = time_list[1];
	bank_time = time_list[2];
	
	if(this.game_state.myTimer != null){
		this.game_state.myTimer.startCountdown(start_time,1000,base_time,bank_time);
	}
	
}

GameController.prototype.got_scores = function(score_list_dict){
	this.game_state.score_textbox_p0.text = score_list_dict["score_list"][0];
	this.game_state.score_textbox_p1.text = score_list_dict["score_list"][1];
	this.game_state.score_textbox_p2.text = score_list_dict["score_list"][2];
	this.game_state.score_textbox_p3.text = score_list_dict["score_list"][3];
}

GameController.prototype.got_discard = function(card_player_dict){
	var trick_id = card_player_dict["id"];
	var relative_player_seat = this.get_relative_seat(card_player_dict["player"],this.game_state.player_pos);
	var card = Card.CardsFromJSON(card_player_dict["card"])[0];
	var discard_pile = this.game_state.trick_group.getByName(trick_id.toString());
	this.game_state.hand_group.children[relative_player_seat].passToCardGroup([card],discard_pile);
}

GameController.prototype.got_valid_cards = function(card_str){
	this.game_state.valid_cards = Card.CardsFromJSON(card_str);
}

GameController.prototype.is_card_valid = function(card){
	for(var i = 0; i < this.game_state.valid_cards.length; i++){
		if(card.equals(this.game_state.valid_cards[i])){
			return true;
		}
	}
	return false;
}

GameController.prototype.got_cards = function(card_str) {
    cards = Card.CardsFromJSON(card_str);
    this.game_state.player_cards = cards
    this.game_state.hand_group.children[0].updateCardState(this.game_state.player_cards,500);
    if (cards.length == 13){
    	this.game_state.hand_group.children[1].fillWithFaceDowns(13,500);
    	this.game_state.hand_group.children[2].fillWithFaceDowns(13,500);
    	this.game_state.hand_group.children[3].fillWithFaceDowns(13,500);
    }
    
}

GameController.prototype.new_game_phase = function(phase) {
	this.game_state.phase = phase;
	if (this.game_state.phase == PASS_PHASE ){
		my_turn = false;
		cards_to_select = 3;
		selected_cards = [];
	}
	if (this.game_state.phase == IN_TRICK) {
		cards_to_select = 1;
		selected_cards = [];
	}
}

GameController.prototype.trick_update = function(trick_dict) {
	var trick_id = trick_dict['id'];
	var relative_player_seat = this.get_relative_seat(trick_dict["player"],this.game_state.player_pos);
	var time_info = trick_dict['time_info'];
	var trick_group = this.game_state.trick_group;
	if (trick_group.countLiving() > 1){
		var to_die = this.game_state.trick_group.countLiving() -1;
		for (var i=0; i<to_die; i++){
			trick_group.children[i].alive = false;
		}
	}
	trick_group.forEachDead(trick_group.remove, trick_group, true, true);
	if (trick_group.getByName(trick_id.toString()) == undefined){
		var location = new Phaser.Point(300,200);
		var scale_factor = new Phaser.Point(0.7,0.7);
		var pile = trick_group.addChild(new DiscardPile(this.game_state.game_board,relative_player_seat,100,5,8,15));
		pile.name = trick_id.toString();
		location.copyTo(pile.position);
		scale_factor.copyTo(pile.scale);
	}
	if (relative_player_seat ==0){
		this.game_state.turn_id = trick_id;
		this.game_state.my_turn = true;
		this.got_time_info(time_info);
	}else{
		this.game_state.my_turn = false;
	}
}


GameController.prototype.all_cards_selected = function() {
	var short_cards = [];
	for (card in selected_cards) {
		card = selected_cards[card];
		short_cards.push(card.toJSON());
	}
	this.game_state.my_turn = false;
	if (game_state == PASS_PHASE) {
		tx_multiplexed_packet("game",{'pass_cards_selected': {'received_cards':short_cards, 'turn_id':turn_id}});
	}
	if (game_state == IN_TRICK) {
		tx_multiplexed_packet("game",{'trick_card_selected': {'received_cards':short_cards, 'turn_id':turn_id}});	
	}
	this.game_state.myTimer.stop();
}