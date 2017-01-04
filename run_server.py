#!/usr/bin/env python
# This file was inspired by:
# http://codysoyland.com/2011/feb/6/evented-django-part-one-socketio-and-gevent/
# and 
# http://www.pixeldonor.com/2014/jan/10/django-gevent-and-socketio/

import os

import django.core.handlers.wsgi
import django.core.wsgi
import django
from socketio.server import SocketIOServer

def main():
    PORT=8000

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lessthan3s.settings")

    #django.setup()
    #application = django.core.handlers.wsgi.WSGIHandler()
    application = django.core.wsgi.get_wsgi_application()



    SocketIOServer(('', PORT), application, resource='socket.io').serve_forever()

if __name__ == '__main__':
    main()
