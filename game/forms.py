from game.models import Player, Character
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = Player
        fields = ["username", "email", "password1", "password2"]

class EditProfileForm(UserChangeForm):
    class Meta:
        model = Player
        fields = ["username","email"]

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'character_class']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter character name'}),
        }
