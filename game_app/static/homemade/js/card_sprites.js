var DEFAULT_SCALE_X = .4;
var DEFAULT_SCALE_Y = .4;

function create_sprite_for_card(card) {}

function create_facedown_card(game, x, y) {
    sprite =  game.add.sprite( x, y, Card.CLUBS, 14);
    sprite.scale.set(DEFAULT_SCALE_X, DEFAULT_SCALE_Y);
    return sprite;
}

function create_card_sprite(game, x, y, card) {
    sprite =  game.add.sprite( x, y, card.suit, card.number - 1);
    sprite.scale.set(DEFAULT_SCALE_X, DEFAULT_SCALE_Y);
    return sprite;
}
    
    
    
