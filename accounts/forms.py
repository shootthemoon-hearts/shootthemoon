from django.contrib.auth import authenticate
from django import forms

class LogInForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'type':'password'}))
    
    def clean(self):
        cleaned_data = super(LogInForm, self).clean()
        self.user = authenticate(username=cleaned_data['user_name'], password=cleaned_data['password'])
        if self.user is None:
            raise forms.ValidationError(
                "Login failed"
            )
            

class SignUpForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'type':'password'}))
    