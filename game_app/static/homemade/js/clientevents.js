/**
 * This file sends updates to the server when 
 * the player makes a move, and receives new states from the server.
 */

// Not sure what these next few lines do
;
jQuery(function($){    
    'use strict';

    /**
     * Namespace responsible for binding events to the proper functions
     */
    var IO = {

        /**
         * This is called when the page is displayed. It connects the Socket.IO 
         * client to the Socket.IO server
         */
        init: function() {
	    IO.socket = new WebSocket("ws://" + window.location.host);
	    IO.bindevents();
        },
       
	bindevents: function() {
	    IO.socket.onmessage = function(message) {
                console.log(message.data);
            }
        }

    };
    IO.init();
    createGame(IO);
});
