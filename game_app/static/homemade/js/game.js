BEFORE_GAME = "BEFORE_GAME";
PASS_PHASE = "PASS_PHASE";
IN_TRICK = "IN_TRICK";



var game_board = null;
var player_cards = [];
var player_pos = null;
var selected_cards = [];
var my_turn = true;
var cards_to_select = 3;



var game_state = BEFORE_GAME;


function init_game() {

    register_event_handler("Cards", got_cards);
    register_event_handler("player_pos", got_player_pos);
    register_event_handler("game_phase", new_game_phase);
    register_event_handler("your_turn", now_my_turn);
	game_board = createGame();
};

function got_cards(card_str) {
    cards = Card.CardsFromJSON(card_str);
    player_cards = cards;
    show_facedown_cards(game_board, player_cards);
};

function got_player_pos(player) {
    player_pos = player;
};

function new_game_phase(phase) {
	game_state = phase;
	if (game_state == PASS_PHASE ){
		my_turn = true;
		cards_to_select = 3;
		selected_cards = [];
	}
	if (game_state == IN_TRICK) {
		my_turn = false;
		cards_to_select = 1;
		selected_cards = [];
	}
}

function now_my_turn(is_my_turn) {
	my_turn = is_my_turn;
}

function all_cards_selected() {
	var short_cards = [];
	for (card in selected_cards) {
		card = selected_cards[card];
		short_cards.push( card.toJSON());
	}
	my_turn = false;
	if (game_state == PASS_PHASE) {
		socket.send(JSON.stringify({'pass_cards_selected': short_cards}));
	}
	if (game_state == IN_TRICK) {
		socket.send(JSON.stringify({'trick_card_selected': short_cards}));
	}
}