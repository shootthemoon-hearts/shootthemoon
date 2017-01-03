from django.shortcuts import render

def index(request):
    #socketio = request.environ['socketio']
    return render(request, 'heartsgame/index.html', context = {})   

