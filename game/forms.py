from game.models import Player, Character
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms 

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
        model = Character  # Используем модель Character
        fields = ['name', 'character_class']  # Поля, которые будут отображены в форме создания персонажа
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя персонажа'}),  # Виджет для поля имени
        }
