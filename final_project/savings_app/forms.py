from django import forms
from .models import AppUsers, Category


def number_validator(number):
    if not number > 0:
        raise forms.ValidationError("Your number must be positive")


class AddExpenseForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects, empty_label=None)
    price = forms.DecimalField(decimal_places=2, min_value=0, validators=[number_validator])
    expense_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))


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


class AddBudgetForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    amount = forms.DecimalField(decimal_places=2, min_value=0, validators=[number_validator])
    category = forms.ModelChoiceField(queryset=Category.objects, empty_label=None)