var DiscardPile = function(game,initial_relative_seat,radius_mean,radius_std_dev,position_angle_std_dev,facing_angle_offset_std_dev) {
	CardGrouping.call(this, game);
	this.relative_seat_discard_positions = [];
	this.relative_seat_discard_angles = [];
	this.initial_relative_seat = initial_relative_seat;
	
	var unit_vector = new Phaser.Point(1,0);
	
	for (var position_ind=0; position_ind<4; position_ind++){
		var current_base_angle = ((position_ind+initial_relative_seat)%4) * 90;
		
		var current_facing_angle = DiscardPile.UniformRandom(current_base_angle,facing_angle_offset_std_dev);
		this.relative_seat_discard_angles.push(current_facing_angle);
		
		var current_radius = DiscardPile.UniformRandom(radius_mean,radius_std_dev);
		var current_position_angle = DiscardPile.UniformRandom(-current_base_angle,position_angle_std_dev);
		var current_position = Phaser.Point.rotate(unit_vector,0,0,current_position_angle,true,current_radius);
		this.relative_seat_discard_positions.push(current_position);
	}	
}

DiscardPile.UniformRandom = function(mean,std_dev){
	return (Math.random()-0.5)*4*std_dev + mean;
}
DiscardPile.prototype = Object.create(CardGrouping.prototype);
DiscardPile.prototype.constructor = CardGrouping;

DiscardPile.prototype.getPoints = function(numberOfCards){
	//numberOfCards is ignored
	return this.relative_seat_discard_positions;
}
DiscardPile.prototype.getAngles = function(numberOfCards){
	//numberOfCards is ignored
	return this.relative_seat_discard_angles;
}

DiscardPile.prototype.sortCards = function(){}	//do nothing, cards always retain original order in a discard pile

DiscardPile.prototype.dematerializeTowards = function(angle){
	this.parent.remove(this,true,true);
}



