var TweenCapsule = function(game,child){
	Phaser.Group.call(this, game);
	this.add(child);
	this.tweens = new Phaser.ArraySet();
}

TweenCapsule.prototype = Object.create(Phaser.Group.prototype);
TweenCapsule.prototype.constructor = TweenCapsule;


//static functions =================================
TweenCapsule.relativeGeometry = function(object,object_base){
	return {
		'position':Phaser.Point.subtract(object.worldPosition,object_base.worldPosition).rotate(0,0,-object_base.worldRotation),
		'rotation':object.worldRotation - object_base.worldRotation,
		'scale':   new Phaser.Point(1,1),
		//'scale':   Phaser.Point.divide(object.worldScale,object_base.worldScale),
	}
}

TweenCapsule.forceRelativeGeometry = function(object,object_base){
	var geometry = this.relativeGeometry(object,object_base);
	object.position= geometry['position'];
	object.rotation= geometry['rotation'];
	object.scale   = geometry['scale'];
}

TweenCapsule.makeTween = function(game,object,object_to_match,duration,position_easing,rotation_easing,scale_easing,object_base=object.parent){
	var target = TweenCapsule.relativeGeometry(object_to_match,object_base);
	var move_tween = game.add.tween(object);
	var rotation_tween = game.add.tween(object);
	var scale_tween = game.add.tween(object.scale);	
	
	move_tween.to({'x':target['position'].x,'y':target['position'].y}, duration, position_easing);
	//doesn't work
	var equiv_rotation = (target['rotation']-object.rotation + Math.PI)%Phaser.Math.PI2 - Math.PI + object.rotation;
	rotation_tween.to({'rotation':equiv_rotation}, duration, rotation_easing);
	scale_tween.to({'x':target['scale'].x,'y':target['scale'].y},duration,scale_easing);
	
	move_tween.start();
	rotation_tween.start();
	scale_tween.start();
	
	return [move_tween,rotation_tween,scale_tween];
}

//member functions mirroring static functions===================
TweenCapsule.prototype.relativeGeometry = function(object){
	return TweenCapsule.relativeGeometry(object,this);
}

TweenCapsule.prototype.forceRelativeGeometry = function(object){
	TweenCapsule.forceRelativeGeometry(object,this);
}

TweenCapsule.prototype.makeTween = function(object_to_match,duration,position_easing,rotation_easing,scale_easing){
	var tweens = TweenCapsule.makeTween(this.game,this.children[0],object_to_match,duration,position_easing,rotation_easing,scale_easing,this);
	this.listenToTweens(tweens);
	return tweens;
}

//other member functions =======================================

TweenCapsule.prototype.switchToParent = function(new_parent,index,silent=false){
	TweenCapsule.forceRelativeGeometry(this,new_parent);
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
	TweenCapsule.forceRelativeGeometry(this.children[0],this.parent);
	this.parent.add(this.children[0],silent,this.z);
	this.parent.remove(this,true,silent);
}











