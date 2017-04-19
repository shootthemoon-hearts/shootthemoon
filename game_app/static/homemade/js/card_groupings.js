var CardGrouping = function(game) {
	Phaser.Group.call(this, game);
}

CardGrouping.prototype = Object.create(Phaser.Group.prototype);
CardGrouping.prototype.constructor = CardGrouping;
CardGrouping.prototype.classType = CardSprite;

CardGrouping.prototype.materialize = function(card_sprites,x,y,relativeFlag=true,forward=true){
	var card_sprite, move_tween, vis_tween, destPoint;
	for (i=0;i<card_sprites.length;i++){
		card_sprite = card_sprites[i];
		move_tween = this.game.add.tween(card_sprite);
		vis_tween = this.game.add.tween(card_sprite);
			
		if (relativeFlag){
			destPoint = Phaser.Point.add(new Phaser.Point(x,y),new Phaser.Point(card_sprite.x,card_sprite.y));
		}else{
			destPoint = new Phaser.Point(x,y);
		}
		
		if (forward){
			move_tween.from({x:destPoint.x,y:destPoint.y}, 1000, Phaser.Easing.Cubic.Out);
			vis_tween.from({alpha:0} , 1000, Phaser.Easing.Linear.None);
			card_sprite.visible = true;
		}else{
			move_tween.to({x:destPoint.x,y:destPoint.y}, 1000, Phaser.Easing.Cubic.Out);
			vis_tween.to({alpha:0} , 1000, Phaser.Easing.Linear.None);
			vis_tween.onComplete.add(function(sprite,tween){sprite.destroy},sprite);
		}
		move_tween.start();
		vis_tween.start();
	}
}

CardGrouping.prototype.dematerialize = function(card_sprites,x,y,relativeFlag=true){
	var forward = false;
	this.materialize(card_sprites,x,y,relativeFlag,forward);
}

CardGrouping.prototype.getPoints = function(number_of_cards){
	var result = new Array();
	for (i=0;i<number_of_cards;i++){
		result.push(new Phaser.Point(0,0));
	}
	return result;
}

CardGrouping.prototype.getPointsByCardSprite = function(card_sprites){
	var all_points = this.getPoints(this.countLiving());
	var result = [];
	for (i=0;i<card_sprites.length;i++){
		var dead_sprites_below = this.filter(function(child,ind,all){return !child.alive && child.z<card_sprites[i].z}).list;
		result.push(all_points[card_sprites[i].z-dead_sprites_below.length]);
	}
	return result;
}


CardGrouping.prototype.applyPositions = function(card_sprites){
	var destPoints = this.getPointsByCardSprite(card_sprites);
	for (i=0;i<card_sprites.length;i++){
		card_sprites[i].x = destPoints[i].x;
		card_sprites[i].y = destPoints[i].y;
	}
}

CardGrouping.prototype.slideToPositions = function(card_sprites){
	var destPoints = this.getPointsByCardSprite(card_sprites);
	for (i=0;i<card_sprites.length;i++){
		var move_tween = this.game.add.tween(card_sprites[i]);
		move_tween.to({x:destPoints[i].x,y:destPoints[i].y}, 1000, Phaser.Easing.Cubic.Out);
		move_tween.start();
	}
}

CardGrouping.prototype.ghostAddCards = function(cards){
	var created_sprites = [];
	for (i=0;i<cards.length;i++){
		var new_sprite = this.create(0,0,cards[i].suit,cards[i].number);
		new_sprite.visible = false;
		created_sprites.push(new_sprite);
	}
	return created_sprites;
}

CardGrouping.prototype.updateCardState = function(cards){
	var cards_to_create = [];
	this.setAll('alive',false);
	for (i=0;i<cards.length;i++){
		var match_found = false;
		var available_cards = this.children; //could use this.filter instead for shorter list
		for (j=0;j<available_cards.length;j++){
			if (!available_cards[j].alive && 
					cards[i].suit == available_cards[j].card.suit && 
					cards[i].number == available_cards[j].card.number ){
				match_found = true;
				available_cards[j].alive = true;
			}
		}
		if (!match_found){
			cards_to_create.push(cards[i]);
		}
	}
	
	var cards_to_slide  = this.filter(function(child,ind,all){return  child.alive},true).list;
	var cards_to_delete = this.filter(function(child,ind,all){return !child.alive},true).list;
	
	cards_to_create = this.ghostAddCards(cards_to_create);
	this.sort('wat',Phaser.Group.SORT_ASCENDING);
	this.applyPositions(cards_to_create);
	this.materialize(cards_to_create,0,-10);
	
	this.dematerialize(cards_to_delete,0,10);

	this.slideToPositions(cards_to_slide);
}

CardGrouping.prototype.revealAll = function(){
	this.callAll('reveal',null);
}

CardGrouping.prototype.hideAll = function(){
	this.callAll('flipToShallow',null,'Back',0);
}

CardGrouping.prototype.deepHideAll = function(){
	this.callAll('flipTo',null,'Back',0);
}

