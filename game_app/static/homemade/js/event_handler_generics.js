function generic_event_handler(){
	this.key_to_handler_dict = {};
	this.register_handler = function (key,handler){
		this.key_to_handler_dict[key] = handler;
	}
}

function value_is_key_event_handler(key_key,payload_key){
	this.parent = new generic_event_handler();
	this.act_on = function(dict){
		var key = dict[key_key];
		var payload = dict[payload_key];
		if (this.parent.key_to_handler_dict.hasOwnProperty(key)) {
            var handler = this.parent.key_to_handler_dict[key];
            handler(payload);
        }
    }
}

function key_is_key_event_handler(){
	this.parent = new generic_event_handler();
	this.act_on = function(dict){
		for (key in dict) {
			var payload = dict[key];
	        if (this.parent.key_to_handler_dict.hasOwnProperty(key)) {
	        	var handler = this.parent.key_to_handler_dict[key];
	        	handler(payload);
	        }
		}
    }
}