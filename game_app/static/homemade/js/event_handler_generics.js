function generic_event_handler(){
	var key_to_handler_dict = {};
	this.register_handler = function (key,handler){
		key_to_handler_dict[key] = handler;
	}
}

function value_is_key_event_handler(key_key,payload_key,context){
	var key_to_handler_dict = {};
	this.register_handler = function (key,handler, context){
		key_to_handler_dict[key] = [handler, context];
	}
	this.act_on = function(dict){
		var key = dict[key_key];
		var payload = dict[payload_key];
		if (key_to_handler_dict.hasOwnProperty(key)) {
			var handler_info = key_to_handler_dict[key];
			handler = handler_info[0];
			context = handler_info[1];
			handler.apply(context, [payload]);
        }
    }
}

function key_is_key_event_handler(){
	var key_to_handler_dict = {};
	this.register_handler = function (key,handler,context){
		key_to_handler_dict[key] = [handler, context];
	}
	this.act_on = function(dict){
		for (var key in dict) {
			var payload = dict[key];
	        if (key_to_handler_dict.hasOwnProperty(key)) {
	        	var handler_info = key_to_handler_dict[key];
	        	handler = handler_info[0];
	        	context = handler_info[1];
	        	handler.apply(context, [payload]);
	        }
		}
    }
}