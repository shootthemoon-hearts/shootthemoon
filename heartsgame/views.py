from django.shortcuts import render

def index(request):
    return render(request, 'heartsgame/index.html', context = {})   

