from django.shortcuts import render

def index(request):
    return render(request, 'game_app/index.html', context = {})   
