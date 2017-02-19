BEFORE_GAME = "BEFORE_GAME";
PASS_PHASE = "PASS_PHASE";
IN_TRICK = "IN_TRICK";


var game_board = null;
var player_cards = [];
var player_pos = null;
var selected_cards = [];



var game_state = BEFORE_GAME;


function init_game() {

    register_event_handler("Cards", got_cards);
    register_event_handler("player_pos", got_player_pos);
    register_event_handler("game_phase", new_game_phase);
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
}

function all_cards_selected() {
	var short_cards = [];
	for (card in selected_cards) {
		card = selected_cards[card];
		short_cards.push( card.toJSON());
	}
	socket.send(JSON.stringify({'pass_cards_selected': short_cards}));
}