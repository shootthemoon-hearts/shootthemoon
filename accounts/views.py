from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect

from accounts.forms import LogInForm
from accounts.forms import SignUpForm

from game_app.models.account import Account

def log_in(request):
    '''Returns a rendered html page the user can use to log in to their
    account. Will send the user to the home page after successful log in. If
    the log in is unsuccessful, the user will be sent back to the log in page
    with an error message displayed at the top.

    Arguments:
        request: the request sent by the user
    '''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LogInForm(request.POST)
        if form.is_valid():
            auth.login(request, form.user)
            # Send the user back to the home page
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    # TODO: I took this from the example, but I'm not quite sure if we want it
    else:
        form = LogInForm()

    return render(request, 'accounts/login.html', {'form': form})

def sign_up(request):
    '''Returns a rendered html page the user can use to sign up for an
    account. Currently does not validate the sign up information.

    Arguments:
        request: the request sent by the user
    '''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # TODO: Issue #27 Add proper verification
        if form.is_valid():
            user = User.objects.create_user(form.data['user_name'], None, form.data['password'])
            Account.objects.create(user=user)
            auth.login(request,user)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    # TODO: I took this from the example, but I'm not quite sure if we want it
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def log_out(request):
    '''Logs the user out of their account and sends them back to the home
    page. Does not check to see if the user is currently logged in.

    Arguments:
        request: the request sent by the user
    '''
    auth.logout(request)
    return HttpResponseRedirect('/')
