var Hand = function(game_controller,gap,offset,hand_position) {
	CardGrouping.call(this, game_controller);
    this.gap = gap;
    this.offset = offset;
    this.hand_position = hand_position;
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
	sprite.tint = 0xFFFFFF;
}

Hand.prototype.cardSelected = function(sprite) {
	if (this.isCardValid(sprite.parent.card)){
		this.discardCard(sprite.parent.card);
	}
}

Hand.prototype.discardCard = function(card) {
	this.game_controller.discard_trick_cards([card]);
}

Hand.prototype.isCardValid = function (card) {
	if (this.game_controller.game_state.relative_player_seat == this.hand_position && 
		this.game_controller.game_state.player_pos == this.hand_position) {
		if (this.game_controller.game_state.phase == GameState.IN_TRICK) {
			return true;
		}
	}
	return false;
	
}


