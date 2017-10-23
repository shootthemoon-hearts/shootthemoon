var Timer = function(game, game_state){
	this.game = game;
	this.game_state = game_state;
	this.tick = 0;
	this.base_ms = 0;
	this.bank_ms = 0;
	this.initialCountdown = 0;
	this.daTimer = null;
	this.textDisplay = new Phaser.Text(game, 400, 400, "");
	this.textDisplay.fill = "red";
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
	this.initialCountdown = Math.ceil(this.total_ms / this.tick);
	this.daTimer = this.game.time.create(true);
	this.daTimer.repeat(this.tick,this.initialCountdown,this.updateTimer,this);
	this.daTimer.start();
}

Timer.prototype.updateTimer = function(){
	this.updateText();
}

Timer.prototype.updateText = function(){
	if(this.game_state.my_turn == true){
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

		base_str = Math.ceil(base_ms/1000).toString();

		if (bank_ms != undefined) {
			bank_str = Math.ceil(bank_ms/1000).toString();
			this.textDisplay.text = base_str + "+" + bank_str;
		} else {
			this.textDisplay.text = base_str;
		}
	} else {
		this.textDisplay.text = "";
	}
}

