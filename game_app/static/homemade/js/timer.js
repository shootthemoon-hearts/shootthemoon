var Timer = function(game){
	this.game = game;
	this.tick = 0;
	this.base_ms = 0;
	this.bank_ms = 0;
	this.total_ms = 0;
	this.initialCountdown = 0;
	this.daTimer = null;
	this.textDisplay = new Phaser.Text(game, 400, 400, "");
	this.textDisplay.fill = "red";
	//this.textDisplay.font = "Arial"; //doesn't work and idk how to do it yet.
}

Timer.prototype.stop = function(){
	if(this.daTimer != null){
		this.daTimer.destroy();
	}
}

Timer.prototype.startCountdown = function(start_time, tick, base_ms, bank_ms){
	this.stop();
	this.start_time = start_time;
	this.tick = tick;
	this.base_ms = base_ms;
	this.bank_ms = bank_ms;
	this.total_ms = this.base_ms + this.bank_ms;
	this.end_time = this.start_time + this.total_ms;
	this.initialCountdown = Math.floor(this.total_ms / this.tick);
	this.daTimer = this.game.time.create(true);
	this.daTimer.repeat(this.tick,this.initialCountdown,this.updateTimer,this);
	this.daTimer.start();
	//this.updateTimer
}

Timer.prototype.updateTimer = function(){
	this.updateText();
}

Timer.prototype.updateText = function(){
	if(my_turn == true){
		var current_time = new Date();
		//console.log("end_time" + this.end_time);
		//console.log("current_time" + current_time);
		var time_left = this.end_time - current_time;
		var base_ms = time_left - this.bank_ms;
		var bank_ms = this.bank_ms;
		if(base_ms < 0){
			base_ms = 0;
		}
		if(base_ms == 0){
			bank_ms = time_left;
			if(bank_ms < 0){
				bank_ms = 0;
			}
		}
		this.textDisplay.text = (Math.ceil(base_ms/1000)).toString() + "+" + (Math.ceil(bank_ms/1000)).toString();
	} else {
		this.textDisplay.text = ""
	}
}

