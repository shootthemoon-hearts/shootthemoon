BEFORE_GAME = "BEFORE_GAME";
PASS_PHASE = "PASS_PHASE";
IN_TRICK = "IN_TRICK";


var game_board = null;
var player_cards = [];
var player_pos = null;



var game_state = BEFORE_GAME;


function init_game() {

    register_event_handler("Cards", got_cards);
    register_event_handler("player_pos", got_player_pos);
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