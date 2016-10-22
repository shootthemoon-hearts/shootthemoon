;
jQuery(function($){    
    'use strict';
    console.log("in jquery");

    /**
     * All the code relevant to Socket.IO is collected in the IO namespace.
     *
     * @type {{init: Function, bindEvents: Function, onConnected: Function, onNewGameCreated: Function, playerJoinedRoom: Function, beginNewGame: Function, onNewWordData: Function, hostCheckAnswer: Function, gameOver: Function, error: Function}}
     */
    var IO = {

        /**
         * This is called when the page is displayed. It connects the Socket.IO client
         * to the Socket.IO server
         */
        init: function() {
            IO.socket = io.connect();
            IO.bindEvents();
        },

        /**
         * While connected, Socket.IO will listen to the following events emitted
         * by the Socket.IO server, then run the appropriate function.
         */
        bindEvents : function() {
            IO.socket.on('connected', IO.onConnected );
        },
        
        /**
         * The client is successfully connected!
         */
        onConnected : function() {
        	console.log("Connected!");
            // Cache a copy of the client's socket.IO session ID on the App
//            App.mySocketId = IO.socket.socket.sessionid;
            // console.log(data.message);
        }
    };
    
    IO.init();

	var game = new Phaser.Game(800, 600, Phaser.AUTO, '', { preload: preload, create: create, update: update });

	function preload() {
		game.load.image('tile', '../third_party/assets/mahjong-icon.png');
	}
	function create () {
		createFakeHand();
		createMostDynamicGameBoardEver();
	}

	function update() {
		
	}

	function createFakeHand() {
		var hands = [];
		var num_players = 4;
		var num_tiles = 13;
		for (var i = 0; i < num_players; i++) {
			var tiles = []
			for (var tile_idx = 0; tile_idx < num_tiles; tile_idx++){
				var value = Math.floor(Math.random() * (9 - 0)) + 0;
				var suit = "sou";
				tiles[tile_idx] = new Tile(suit, value);
			}

			hands[i] = new Hand(tiles);
		}

		var hand_str = '';
		for (i = 0; i < num_tiles; i++) {
			hand_str += hands[0].tiles[i].value;
		}
	}

	function createMostDynamicGameBoardEver() {

		var array = (function() {
			var array = [];
			for (var i = 0; i < 13; i++) {
				array.push('tile');
			}
			return array;
		})();
		console.log(array[0]);
		fillHorizontalText(array, 50, 50, 400);
		fillHorizontalText(array, 375, 50, 400);

		fillVerticalText(array, 10, 70, 380);
		fillVerticalText(array, 410, 70, 380);


	}

	function fillHorizontalText(text, y, start_x, end_x) {
		text = Array.from(text);
		for (var i = 0; i < text.length; i++) {
			var x = ((end_x - start_x) / text.length * i) + start_x;

			var sprite = game.add.sprite(x, y, text[i]);
			// Also enable sprite for drag
			sprite.inputEnabled = true;
			sprite.input.enableDrag();
			sprite.events.onDragStart.add(startDrag, this);
			sprite.events.onDragStop.add(stopDrag, this);
		}
	}

	function fillVerticalText(text, x, start_y, end_y) {
		text = Array.from(text);
		for (var i = 0; i < text.length; i++) {
			var y = ((end_y - start_y) / text.length * i) + start_y;

			var sprite = game.add.sprite(x, y, text[i]);
			// Also enable sprite for drag
			sprite.inputEnabled = true;
			sprite.input.enableDrag();
			sprite.events.onDragStart.add(startDrag, this);
			sprite.events.onDragStop.add(stopDrag, this);
		}
	}

	function startDrag() {
		console.log("Drag Started");
	}

	function stopDrag() {
		console.log("Drag Stopped");
		IO.socket.emit('tileDragged');
	}
});