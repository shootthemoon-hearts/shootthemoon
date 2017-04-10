var CardGrouping = function(game) {
	Phaser.Group.call(this, game);
};

var dematerialize = function(indices,x,y,relativeFlag=true){
	var sprite, move_tween, vis_tween, xdest, ydest;
	for (index of indices){
		sprite = this.children[index];
		move_tween = this.game.add.tween(sprite);
		vis_tween = this.game.add.tween(sprite);
			
		if (relativeFlag){
			xdest = x + sprite.x;
			ydest = y + sprite.y;
		}else{
			xdest = x;
			ydest = y;
		}
		
		move_tween.to({x:xdest,y:ydest}, 1000, Phaser.Easing.Cubic.Out,true,0,0,false);
		vis_tween.to({alpha:0} , 1000, Phaser.Easing.Linear.None,false,0,0,false);
		vis_tween.onComplete.add(sprite.destroy,null);
		vis_tween.start();
	}
};


CardGrouping.prototype = Object.create(Phaser.Group.prototype);
CardGrouping.prototype.constructor = CardGrouping;
CardGrouping.prototype.dematerialize = dematerialize;
//CardGrouping.prototype.materialize
//CardGrouping.prototype.updateCardListState
//CardGrouping.prototype.passCards
