

// Main:
(function () {
	createFakeHand();
	createMostDynamicGameBoardEver();
}) ();

function createFakeHand() {
	var hands = [];
	var num_players = 4;
	var num_tiles = 13;
	for (i = 0; i < num_players; i++) {
		var tiles = []
		for (tile_idx = 0; tile_idx < num_tiles; tile_idx++){
			value = Math.floor(Math.random() * (9 - 0)) + 0;
			suit = "sou";
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
	var canvas = document.getElementById('board');
	var context = canvas.getContext('2d');
	context.font = '30pt Calibri, sans-serif';

	context.fillText('🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀', 50, 50);
	context.fillText('🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀', 50, 550);

	fillVerticalText('🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀', 10, 55, 575);
	fillVerticalText('🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀🀀', 470, 55, 575);


	function fillVerticalText(text, x, start_y, end_y) {
		text = Array.from(text);
		for (i = 0; i < text.length; i++) {
			var y = ((end_y - start_y) / text.length * i) + start_y;

			context.fillText(text[i], x, y);
		}
	}
}