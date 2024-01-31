from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('participant', 'Participant'),
        ('creator', 'Creator'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='participant',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type']


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'profile_picture', 'birth_date', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }
