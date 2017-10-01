# Shoot The Moon

The current code uses [Django](https://www.djangoproject.com/) as the server, [Django Channels](https://channels.readthedocs.io/en/stable/) to manage client/server communications via [Websockets](https://en.wikipedia.org/wiki/WebSocket), and [Phaser](phaser.io) for the game framework.

The [Redis](redis.io) implementation of channels is used, so Redis must be started on port 6379 before launching Django.

Python 3.6 is required. Using virtualenv to setup Python is recommended.

    virtualenv stm
    source stm/bin/activate
    pip install -r requirements.txt
