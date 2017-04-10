var CardSprite = function(game,x,y,suit,number) {
	Phaser.Sprite.call(this, game,x,y,suit,number);
	this.card = Card(suit,number);
}

var flipTo = function(card){
	tmp_width = this.width;
	half_flip_a = this.game.add.tween(this).to( { width: 0 }, 2000, "Quart.easeOut");
	half_flip_b = this.game.add.tween(this).to( { width: tmp_width }, 2000, "Quart.easeOut");
}
CardSprite.prototype = Object.create(Phaser.Sprite.prototype);
CardSprite.prototype.constructor = CardSprite; 