function generic_event_handler(){
	this.key_to_handler_dict = {};
	this.register_handler = function (key,handler){
		this.key_to_handler_dict[key] = handler;
	}
}

//I don't know how to do inheritence in JS

function value_is_key_event_handler(key_key,payload_key){
	this.key_to_handler_dict = {};
	this.register_handler = function (key,handler){
		this.key_to_handler_dict[key] = handler;
	}
	this.act_on = function(dict){
		var key = dict[key_key];
		var payload = dict[payload_key];
		if (this.key_to_handler_dict.hasOwnProperty(key)) {
            var handler = this.key_to_handler_dict[key];
            handler(payload);
        }
    }
}

function key_is_key_event_handler(){
	this.key_to_handler_dict = {};
	this.register_handler = function (key,handler){
		this.key_to_handler_dict[key] = handler;
	}
	this.act_on = function(dict){
		for (var key in dict) {
			var payload = dict[key];
	        if (this.key_to_handler_dict.hasOwnProperty(key)) {
	        	var handler = this.key_to_handler_dict[key];
	        	handler(payload);
	        }
		}
    }
}