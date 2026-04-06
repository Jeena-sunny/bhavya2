from shop.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
class SignUpForm(UserCreationForm):
    gender_choices = (('male','male'),('female','female'))
    role_choices = (('admin','admin'),('user','user'))

    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect)
    role = forms.ChoiceField(choices=role_choices)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'gender', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)