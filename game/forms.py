from game.models import Player, Character
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms 
from django.core.validators import MinValueValidator, MaxValueValidator

# Форма для регистрации нового пользователя
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Поле для ввода email (обязательно)
    
    class Meta(UserCreationForm.Meta):  # Метаданные формы
        model = Player  # Используем модель Player для создания пользователя
        fields = ["username", "email", "password1", "password2"]  # Поля, которые будут отображены в форме

# Форма для редактирования профиля пользователя
class EditProfileForm(UserChangeForm):
    class Meta:
        model = Player  # Используем модель Player
        fields = ["username", "email"]  # Поля, которые можно редактировать

# Форма для создания нового персонажа
class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'character_class', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter character name'}),
        }
    
    level = forms.IntegerField(
        required=False,  # Сделайте поле необязательным
        validators=[
            MinValueValidator(1, "Level must be at least 1."),
            MaxValueValidator(100, "Level cannot exceed 100.")
        ],
        initial=1  # Устанавливаем начальное значение
    )
