var Hand = function(game_controller,gap,offset,hand_position) {
	CardGrouping.call(this, game_controller);
    this.gap = gap;
    this.offset = offset;
    this.hand_position = hand_position;
    this.selected_cards = [];
}

Hand.prototype = Object.create(CardGrouping.prototype);
Hand.prototype.constructor = Hand; 

Hand.prototype.getPositions = function(numberOfCards){
	var result = new Array();
	for (i=0;i<numberOfCards;i++){
		var x = -(this.offset+(numberOfCards-1)*this.gap)/2 + (i-1)*this.gap;
		result.push(new Phaser.Point(x,0));
	}
	return result;
}

//Hand.prototype.updateCardState = function(cards, duration) {
//	CardGrouping.prototype.updateCardState.call(this, cards, duration);
//	for (i in cards) {
//		cards[i].events.onInputUp.add(discardCard);
//	}
//	
//}

Hand.prototype.mouseOverCard = function(sprite) {
	if (this.isCardValid(sprite.parent.card)){
		sprite.tint = .8 * 0xFF0000;
	}
}

Hand.prototype.mouseOffCard = function(sprite) {
	if (!(this.selected_cards.indexOf(sprite.parent.card) >= 0)) {
		sprite.tint = 0xFFFFFF;
	}
}

Hand.prototype.cardSelected = function(sprite) {
	if (this.isCardValid(sprite.parent.card)) {
		if (this.game_controller.game_state.phase == GameState.IN_TRICK) {
			sprite.tint = 0xFFFFFF;
			this.discardCard(sprite.parent.card);
		} else if (this.game_controller.game_state.phase == GameState.PASS_PHASE) {
			sprite.tint = .8 * 0xFF0000;
			this.selectCardForPass(sprite.parent.card);
		}
	}
}

Hand.prototype.discardCard = function(card) {
	this.game_controller.discard_trick_cards([card]);
}

Hand.prototype.selectCardForPass = function(card) {
	this.selected_cards.push(card);
	if (this.selected_cards.length == this.game_controller.game_state.cards_to_pass) {
		this.game_controller.pass_cards(this.selected_cards);
		this.selected_cards = [];
	}
}

Hand.prototype.isCardSelected = function(card) {
	in_valid_cards = false;
	for (index in this.game_controller.game_state.valid_cards) {
		if (card == this.game_controller.game_state.valid_cards[index]) {
			in_valid_cards = true;
			break;
		}
	}
}

Hand.prototype.isCardValid = function (card) {

	// Checking if the selected card is in our hand, not an opponent's and it's
	// actually our turn
	if (this.game_controller.game_state.player_pos == this.hand_position && 
			this.game_controller.game_state.my_turn) {
		if (this.game_controller.game_state.phase == GameState.IN_TRICK) {
			in_valid_cards = false;
			for (index in this.game_controller.game_state.valid_cards) {
				if (card.equals(this.game_controller.game_state.valid_cards[index])) {
					in_valid_cards = true;
					break;
				}
			}

			if (in_valid_cards) {
				return true;
			}

		} else if (this.game_controller.game_state.phase == GameState.PASS_PHASE) {
				return true;
		}
	}
	return false;
}


