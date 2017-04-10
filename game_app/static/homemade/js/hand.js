var Hand = function(game,gap) {
	CardGrouping.call(this, game);
    this.gap = gap;
    
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
}

Hand.prototype = Object.create(CardGrouping.prototype);
Hand.prototype.constructor = Hand; 