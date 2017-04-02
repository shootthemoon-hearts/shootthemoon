var Hand = function(x,y,gap,offset,rotation) {
	
	this.sprite_group = 
    this.pos = Position(x,y);
    this.gap = gap;
    this.cos = Math.cos(rotation*Math.PI/180);
    this.sin = Math.sin(rotation*Math.PI/180);
    this.number_of_cards = 0;
    
    this.get_card_position(card_index){
    	line_pos = Position(-(this.offset+(this.number_of_cards-1)*this.gap)/2 + (card_index-1)*this.gap,0);
    	return EulerRotate(line_pos,this.cos,this.sin).add(this.pos);
    }
}

var Deck = function(x,y,gap) {
	this.x = x;
	this.y = y;
	this.gap = 1;
	
    this.get_card_position(card_index){
    	return Position(0,(card_index-1)*this.gap).add(this.pos);
    }
}

var DiscardPile = function(x,y,width,height) {
	this.x = x;
	this.y = y;
	this.width = width;
	this.height = height;
    this.get_card_position(card_index){
    	return Position(this.x,this.y);
    }
}