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
            IO.socket = io.connect();
            IO.bindEvents();
        },

        /**
         * Binds the server / client events to the proper functions
         */
        bindEvents : function() {
            IO.socket.on('connected', IO.onConnected );
        },
        
        /**
         * Called when the client is added to a game
         */
        onConnected : function(data) {
        	console.log("Connected!");
        	console.log("id:" + data);
        }
    };
    IO.init();
    createGame();
});