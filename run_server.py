#!/usr/bin/env python3
# This file was inspired by:
# http://codysoyland.com/2011/feb/6/evented-django-part-one-socketio-and-gevent/

import os

import django.core.handlers.wsgi
import django

PORT=8000

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lessthan3s.settings")

django.setup()
application = django.core.handlers.wsgi.WSGIHandler()

from socketio.server import SocketIOServer

if __name__ == '__main__':
    SocketIOServer(('', PORT), application, resource='socket.io').serve_forever()

