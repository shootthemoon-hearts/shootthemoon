var Hand = function(game,gap,offset) {
	CardGrouping.call(this, game);
    this.gap = gap;
    this.offset = offset;
    this.classType = CardSprite;
}
Hand.prototype = Object.create(CardGrouping.prototype);
Hand.prototype.constructor = Hand; 

Hand.prototype.getPoints = function(numberOfCards){
	var result = new Array();
	for (i=0;i<numberOfCards;i++){
		var x = -(this.offset+(numberOfCards-1)*this.gap)/2 + (i-1)*this.gap;
		result.push(new Phaser.Point(x,0));
	}
	return result;
}

    /*this.update_card_list(new_card_list){
    	this.card_list = new_card_list;
    	for (i=0;i<this.card_list.length;i++){
    		MaterializeToCardGrouping(this.card_list[i],Position(50,50),this);
    	}
    }
    
    this.get_card_position(card_index){
    	line_pos = Position(-(this.offset+(this.number_of_cards-1)*this.gap)/2 + (card_index-1)*this.gap,0);
    	return EulerRotate(line_pos,this.cos,this.sin).add(this.pos);
    }*/





