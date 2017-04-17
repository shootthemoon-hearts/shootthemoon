from django.contrib.auth import authenticate
from django import forms

MAX_USERNAME_LENGTH=100
MAX_PASSWORD_LENGTH=50

class LogInForm(forms.Form):
    '''This is the form that users will see when they go to log in to their
    account.'''
    user_name = forms.CharField(label='Username', 
                                max_length=MAX_USERNAME_LENGTH)
    
    password_form = forms.TextInput(attrs={'type':'password'})
    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH, 
                               widget=password_form)

    def clean(self):
        '''This function validates the input the user enters when trying to
        log in. The validation will not currently happen enter the user hits
        the Submit button
        
        Raises:
            ValidationError: If the user authentication information the user
                entered is incorrect.
        '''
        cleaned_data = super(LogInForm, self).clean()
        self.user = authenticate(username=cleaned_data['user_name'], 
                                 password=cleaned_data['password'])
        if self.user is None:
            raise forms.ValidationError("Login failed")


class SignUpForm(forms.Form):
    '''This is the form that users will see when they go to sign up for an
    account'''
    user_name = forms.CharField(label='Username', 
                                max_length=MAX_USERNAME_LENGTH)
    password_form = forms.TextInput(attrs={'type':'password'})
    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH, 
                               widget=password_form)

