var Deck = function(game,gap,duration,deck_size=52) {
	CardGrouping.call(this, game);
	this.gap = gap;
	this.fillWithFaceDowns(deck_size,duration);
}

Deck.prototype = Object.create(CardGrouping.prototype);
Deck.prototype.constructor = Deck;

Deck.prototype.getPositions = function(numberOfCards){
	var result = new Array();
	for (var i=0;i<numberOfCards;i++){
		var y = -((numberOfCards-1-i)*this.gap);
		result.push(new Phaser.Point(0,y));
	}
	return result;
}

Deck.prototype.deal = function(groupingList,duration,slide_duration=duration/4){
	var delay = (duration-slide_duration)/this.children.length;
	for (var i=0;i<this.children.length;i++){
		
	}
}