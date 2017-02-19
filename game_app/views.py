from django.shortcuts import render

def genericWs(request):
    return render(request,'game_app/hanyuu.html',context = {})

def index(request):
    '''Render the index.html file for this app when a client connects to this
    app's index URL (i.e. <website>/game.

    Args:
        request: The request sent from the client
    '''
    # Django is setup to look in the templates directory for this file
    return render(request, 'game_app/index.html', context = {})   
