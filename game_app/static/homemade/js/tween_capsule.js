var TweenCapsule = function(game,child){
	Phaser.Group.call(this, game);
	this.add(child);
	this.tweens = new Phaser.ArraySet();
}

TweenCapsule.prototype = Object.create(Phaser.Group.prototype);
TweenCapsule.prototype.constructor = TweenCapsule;

TweenCapsule.prototype.relativeGeometry = function(object,object_base=this){
	return {
		'position':Phaser.Point.subtract(object.worldPosition,object_base.worldPosition).rotate(0,0,-object_base.worldRotation),
		'rotation':object.worldRotation - object_base.worldRotation,
		'scale':   Phaser.Point.divide(object.worldScale,object_base.worldScale),
	}
}

TweenCapsule.prototype.forceRelativeGeometry = function(object,object_base=this){
	var geometry = this.relativeGeometry(object,object_base);
	object.position = geometry['position'];
	object.rotation= geometry['rotation'];
	object.scale   = geometry['scale'];
}

TweenCapsule.prototype.switchToParent = function(new_parent,index,silent=false){
	this.forceRelativeGeometry(this,new_parent);
	new_parent.add(this,silent,index);
}

TweenCapsule.prototype.listenToTweens = function(tweens){
	for (var i=0;i<tweens.length;i++){
		this.tweens.add(tweens[i]);
		tweens[i].onComplete.add(this.onTweenEnd,this);
	}
}

TweenCapsule.prototype.onTweenEnd = function(tweened_object,tween){
	this.tweens.remove(tween);
	if (this.tweens.total == 0){
		this.finish();
	}
}

TweenCapsule.prototype.finish = function(silent=false){
	this.forceRelativeGeometry(this.children[0],this.parent);
	this.parent.add(this.children[0],silent,this.z);
	this.parent.remove(this,true,silent);
}










