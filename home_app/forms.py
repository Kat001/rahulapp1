from django import forms
from django.contrib.auth.forms import UserCreationForm

from Accounts.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for fieldname in ['sponser','username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = Account
        fields = ['sponser','username','email','password1','password2']
