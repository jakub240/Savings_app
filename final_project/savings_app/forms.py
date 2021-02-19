from django import forms
from .models import AppUsers, CITIES, Category
from django.core.validators import EmailValidator, URLValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

"""class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
"""

class AddUserForm(forms.ModelForm):
    class Meta:
        model = AppUsers
        fields = ['username',
                  'password',
                  "repeat_password",
                  'first_name',
                  'last_name',
                  'email',
                  'date_of_birth',
                  'city'
                  ]
        widgets = {
            'password': forms.PasswordInput
        }
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            msg = "Make sure the passwords are the same!"
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)

"""
class UserPasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password != re_password:
            msg = "Make sure the passwords are the same!"
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)"""


class AddExpenseForm(forms.Form):
    name = forms.CharField()
    description = forms.TextInput()
    category = forms.ModelChoiceField(queryset=Category.objects, empty_label=None)
    price = forms.FloatField()





