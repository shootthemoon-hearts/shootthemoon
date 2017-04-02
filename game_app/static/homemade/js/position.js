var Position = function(x,y){
	this.x = x;
	this.y = y;
	
	this.add = function(position){
		this.x += position.x;
		this.y += position.y;
	}
}

var Cosines = function(rotation){
	this.cosx = Math.cos(rotation*Math.PI/180);
    this.cosy = Math.sin(rotation*Math.PI/180);
}

function EulerRotate(position,cosines){
	return Position(
			cosines.cosx*position.x - cosines.cosy*position.y,
			cosines.cosy*position.x + cosines.cosx*position.y);
}