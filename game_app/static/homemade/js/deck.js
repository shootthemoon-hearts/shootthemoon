var Deck = function(game,gap,duration,delay=0,deck_size=52) {
	CardGrouping.call(this, game);
	this.gap = gap;
	this.fillWithFaceDowns(deck_size,duration,delay);
}

Deck.prototype = Object.create(CardGrouping.prototype);
Deck.prototype.constructor = Deck;

Deck.prototype.getPositions = function(numberOfCards){
	var result = new Array();
	for (var i=0;i<numberOfCards;i++){
		var y = -((i)*this.gap);
		result.push(new Phaser.Point(0,y));
	}
	return result;
}

Deck.prototype.dealNoReveal= function(grouping_list,duration,slide_duration=duration/4){
	var delay = (duration-slide_duration)/this.children.length;
	var group_to_pass_to;
	for (var i=0;i<this.children.length;i++){
		group_to_pass_to = grouping_list[i%grouping_list.length];
		this.passToCardGroup([this.children[i].card],group_to_pass_to,slide_duration,delay*i);
	}
}