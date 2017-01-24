from .game import Game

games = []
def player_connected(channel):
    global games
    game = None
    
    # If no games have been created, create one
    if len(games) == 0:
        game = Game(channel, 1);
        games.append(game);
    else:
        # Check if any of the existing rooms aren't full
        found_game = False;
        for game in games:
            if (game.isFull()):
                found_game = True;
                break;
        
        # They're all full, create a new game
        if not found_game:
            game = Game(channel, len(games) + 1);
            games.append(game);

    game.addPlayer(channel);
