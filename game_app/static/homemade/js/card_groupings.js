var CardGrouping = function(game) {
	Phaser.Group.call(this, game);
}

var dematerialize = function(indices,x,y,relativeFlag=true){
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


CardGrouping.prototype = Object.create(Phaser.Group.prototype);
CardGrouping.prototype.constructor = CardGrouping;
CardGrouping.prototype.dematerialize = dematerialize;
//CardGrouping.prototype.classType = CardSprite.prototype;
//CardGrouping.prototype.materialize
//CardGrouping.prototype.updateCardListState
//CardGrouping.prototype.passCards
