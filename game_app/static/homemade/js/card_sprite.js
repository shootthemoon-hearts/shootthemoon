var CardSprite = function(game,x,y,suit,number) {
	Phaser.Sprite.call(this, game,x,y,suit,number);
	this.card = Card(suit,number);
}

var flipTo = function(suit,number){
	tmp_width = this.width;
	tmp_x = this.x;
	
	half_flip_a = this.game.add.tween(this).to( { width: 0, x:this.x + this.width/2 }, 200, Phaser.Easing.Circular.easeIn);
	half_flip_a.onComplete.add(function(sprite,tween){sprite.loadTexture(suit,number)},this);
	half_flip_b = this.game.add.tween(this).to( { width: tmp_width, x:tmp_x}, 200, Phaser.Easing.Circular.easeIn);
	half_flip_a.chain(half_flip_b);
	half_flip_a.start();
	this.card = new Card(suit,number);
}

CardSprite.prototype = Object.create(Phaser.Sprite.prototype);
CardSprite.prototype.constructor = CardSprite;
CardSprite.prototype.flipTo = flipTo;





