var DiscardPile = function(game_controller,initial_relative_seat,radius_mean,radius_std_dev,position_angle_std_dev,facing_angle_offset_std_dev) {
	CardGrouping.call(this, game_controller);
	this.relative_seat_discard_positions = [];
	this.relative_seat_discard_angles = [];
	this.initial_relative_seat = initial_relative_seat;
	
	for (var position_ind=0; position_ind<4; position_ind++){
		var unit_vector = new Phaser.Point(1,0);
		var current_facing_base_angle = ((position_ind+initial_relative_seat)%4) * 90;
		var current_position_base_angle = -current_facing_base_angle -90;
		
		var current_facing_angle = DiscardPile.UniformRandom(current_facing_base_angle,facing_angle_offset_std_dev);
		this.relative_seat_discard_angles.push(current_facing_angle);
		
		var current_radius = DiscardPile.UniformRandom(radius_mean,radius_std_dev);
		var current_position_angle = DiscardPile.UniformRandom(current_position_base_angle,position_angle_std_dev);
		var current_position = Phaser.Point.rotate(unit_vector,0,0,current_position_angle,true,current_radius);
		current_position.setTo(Math.round(current_position.x),Math.round(current_position.y));
		this.relative_seat_discard_positions.push(current_position);
	}	
}

DiscardPile.prototype = Object.create(CardGrouping.prototype);
DiscardPile.prototype.constructor = DiscardPile;

DiscardPile.UniformRandom = function(mean,std_dev){
	return (Math.random()-0.5)*4*std_dev + mean;
}

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



