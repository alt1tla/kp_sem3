from game.models import Player, Character  
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  
from django import forms  
from django.core.validators import MinValueValidator, MaxValueValidator  


# Форма для регистрации нового пользователя
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Поле для ввода email, оно обязательно для заполнения

    class Meta(UserCreationForm.Meta):  # Используем метаданные из UserCreationForm
        model = Player  # Указываем, что форма будет работать с моделью Player
        # Указываем поля, которые должны быть на форме (имя пользователя, email и пароли)
        fields = ["username", "email", "password1", "password2"]  


# Форма для редактирования профиля пользователя
class EditProfileForm(UserChangeForm):
    class Meta:
        model = Player  # Используем модель Player для редактирования данных пользователя
        fields = ["username", "email"]  # Поля, которые можно редактировать 


# Форма для создания нового персонажа
class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character  # Указываем, что форма будет работать с моделью Character
        fields = ['name', 'character_class', 'level']  # Поля формы: имя персонажа, класс и уровень
        widgets = {
            # Устанавливаем placeholder для поля имени персонажа
            'name': forms.TextInput(attrs={'placeholder': 'Enter character name'})}

    level = forms.IntegerField(
        required=False,  # Делаем поле уровня необязательным
        validators=[  # Добавляем валидаторы для уровня
            MinValueValidator(1, "Level must be at least 1."),  # Уровень не может быть меньше 1
            MaxValueValidator(100, "Level cannot exceed 100.")  # Уровень не может быть больше 100
        ],
        initial=1  # Устанавливаем начальное значение уровня равным 1
    )
