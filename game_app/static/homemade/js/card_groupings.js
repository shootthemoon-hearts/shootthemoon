var CardGrouping = function(game) {
	Phaser.Group.call(this, game);
}

CardGrouping.prototype = Object.create(Phaser.Group.prototype);
CardGrouping.prototype.constructor = CardGrouping;

CardGrouping.prototype.dematerialize = function(indices,x,y,relativeFlag=true){
	var sprite, move_tween, vis_tween, xdest, ydest;
	for (index of indices){
		card_sprite = this.children[index];
		move_tween = this.game.add.tween(card_sprite);
		vis_tween = this.game.add.tween(card_sprite);
			
		if (relativeFlag){
			xdest = x + card_sprite.x;
			ydest = y + card_sprite.y;
		}else{
			xdest = x;
			ydest = y;
		}
		
		move_tween.to({x:xdest,y:ydest}, 1000, Phaser.Easing.Cubic.Out,true);
		vis_tween.to({alpha:0} , 1000, Phaser.Easing.Linear.None);
		vis_tween.onComplete.add(function(sprite,tween){sprite.destroy},this);
		vis_tween.start();
	}
}

CardGrouping.prototype.materialize = function(indices,x,y,relativeFlag=true){
	var sprite, move_tween, vis_tween, xdest, ydest;
	for (index of indices){
		card_sprite = this.children[index];
		move_tween = this.game.add.tween(card_sprite);
		vis_tween = this.game.add.tween(card_sprite);
			
		if (relativeFlag){
			xdest = x + card_sprite.x;
			ydest = y + card_sprite.y;
		}else{
			xdest = x;
			ydest = y;
		}
		
		move_tween.to({x:xdest,y:ydest}, 1000, Phaser.Easing.Cubic.Out,true);
		vis_tween.to({alpha:0} , 1000, Phaser.Easing.Linear.None);
		vis_tween.onComplete.add(function(sprite,tween){sprite.destroy},this);
		vis_tween.start();
	}
}

CardGrouping.prototype.getPoints = function(numberOfCards){
	var result = new Array();
	for (i=0;i<numberOfCards;i++){
		result.push(new Phaser.Point(0,0));
	}
	return result;
}

CardGrouping.prototype.applyPositions = function(){
	var points = this.getPoints(this.children.length);
	for (i=0;i<this.children.length;i++){
		this.children[i].x = points[i].x;
		this.children[i].y = points[i].y;
	}
}

CardGrouping.prototype.classType = CardSprite;
//CardGrouping.prototype.materialize
//CardGrouping.prototype.updateCardListState
//CardGrouping.prototype.passCards
