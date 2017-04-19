var CardSprite = function(game,x,y,suit,number) {
	Phaser.Group.call(this, game);
	this.x = x;
	this.y = y;
	this.addChild(new Phaser.Sprite(game,0,0,suit,number));
	this.card = new Card(number,suit);
}

CardSprite.prototype = Object.create(Phaser.Group.prototype);
CardSprite.prototype.constructor = CardSprite;

CardSprite.prototype.flipToShallow = function(suit,number){
	child = this.children[0];//card should be only child
	tmp_width = this.width;
	
	half_flip_a = this.game.add.tween(child).to( { width: 0, x:child.width/2 }, 200, Phaser.Easing.Circular.easeIn);
	half_flip_a.onComplete.add(function(sprite,tween){sprite.loadTexture(suit,number)},this);
	half_flip_b = this.game.add.tween(child).to( { width: tmp_width, x:0}, 200, Phaser.Easing.Circular.easeIn);
	half_flip_a.chain(half_flip_b);
	half_flip_a.start();
}

CardSprite.prototype.flipTo = function(suit,number){
	this.flipToShallow(suit,number);
	this.card = new Card(suit,number);
}

CardSprite.prototype.reveal = function(){
	if (this.key != this.card.suit && this.frame != this.card.number){
		this.flipToShallow(this.card.suit,this.card.number);
	}
}







