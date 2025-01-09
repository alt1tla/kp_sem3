from django.db import models  # Импортируем модуль для работы с моделями Django
from django.contrib.auth.models import AbstractUser  # Импортируем абстрактную модель пользователя
from django.core.exceptions import ValidationError  # Импортируем исключение для валидации

# Модель для представления игроков (пользователей)
class Player(AbstractUser):
    user_id = models.AutoField(primary_key=True)  # Уникальный идентификатор пользователя (auto-generated)
    username = models.CharField(max_length=50, unique=True)  # Имя пользователя, должно быть уникальным
    email = models.EmailField(max_length=100)  # Адрес электронной почты пользователя
    password = models.CharField(max_length=100)  # Пароль пользователя
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания пользователя
    last_login = models.DateTimeField(null=True, blank=True)  # Дата и время последнего входа пользователя

    # Указываем, что для аутентификации будет использоваться поле username
    USERNAME_FIELD = 'username'  
    # Список обязательных полей для создания нового пользователя
    REQUIRED_FIELDS = ['email']  

    def __str__(self):
        return self.username  # Строковое представление пользователя (по имени пользователя)

# Модель для представления классов персонажей
class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название класса (например, "Воин")
    description = models.TextField(blank=True, null=True)  # Описание класса, может быть пустым
    base_health = models.IntegerField(default=100)  # Базовый уровень здоровья для класса
    base_mana = models.IntegerField(default=50)  # Базовый уровень маны для класса

# Модель для представления персонажей
class Character(models.Model):
    character_id = models.AutoField(primary_key=True)  # Уникальный идентификатор персонажа
    user = models.ForeignKey(Player, on_delete=models.CASCADE)  # Связь с игроком (пользователем)
    name = models.CharField(max_length=50)  # Имя персонажа
    level = models.IntegerField()  # Уровень персонажа
    experience = models.IntegerField()  # Опыт персонажа
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)  # Класс персонажа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания персонажа

    def __str__(self):
        return f"{self.name} ({self.character_class.name})"  # Строковое представление персонажа (имя и класс)

    def clean(self):
        super().clean()  # Вызываем родительский метод clean() для сохранения всех стандартных проверок
        # Проверка, что уровень персонажа находится в пределах от 1 до 100
        if not (1 <= self.level <= 100):
            raise ValidationError("Уровень персонажа должен быть в диапазоне от 1 до 100.")

        # Проверка, что имя персонажа уникально для данного пользователя
        if Character.objects.filter(user=self.user, name=self.name).exists():
            raise ValidationError("Персонаж с таким именем уже существует у этого игрока.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Запускаем полную валидацию перед сохранением объекта
        super().save(*args, **kwargs)  # Вызываем метод save() родительского класса

# Модель для представления предметов
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)  # Уникальный идентификатор предмета
    name = models.CharField(max_length=100)  # Название предмета
    description = models.TextField()  # Описание предмета
    type = models.CharField(max_length=50)  # Тип предмета (например, оружие, броня и т.д.)
    rarity = models.CharField(max_length=50)  # Редкость предмета
    value = models.IntegerField()  # Ценность предмета (например, в деньгах или очках)

    def __str__(self):
        return self.name  # Строковое представление предмета (по его названию)

# Модель для связи предметов с персонажами (инвентарь)
class CharacterItem(models.Model):
    character_item_id = models.AutoField(primary_key=True)  # Уникальный идентификатор связи
    character = models.ForeignKey(Character, on_delete=models.CASCADE)  # Связь с персонажем
    item = models.ForeignKey(Item, related_name='character_items', on_delete=models.CASCADE)  # Связь с предметом
    quantity = models.IntegerField()  # Количество данного предмета
    equipped = models.BooleanField(default=False)  # Флаг, указывает, экипирован ли предмет
    acquired_at = models.DateTimeField(auto_now_add=True)  # Дата получения предмета

    def __str__(self):
        return f'{self.character.name} - {self.item.name}'  # Строковое представление связи (персонаж - предмет)

    def clean(self):
        super().clean()  # Вызываем родительский метод clean()
        # Проверка, что количество предметов больше нуля
        if self.quantity <= 0:
            raise ValidationError("Количество предметов должно быть больше нуля.")

# Модель для представления квестов
class Quest(models.Model):
    quest_id = models.AutoField(primary_key=True)  # Уникальный идентификатор квеста
    name = models.CharField(max_length=100)  # Название квеста
    description = models.TextField()  # Описание квеста
    reward = models.CharField(max_length=100)  # Награда за выполнение квеста
    difficulty = models.CharField(max_length=50)  # Сложность квеста
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания квеста

    def __str__(self):
        return self.name  # Строковое представление квеста (по его названию)

# Модель для связи персонажей с квестами (задания персонажей)
class CharacterQuest(models.Model):
    character_quest_id = models.AutoField(primary_key=True)  # Уникальный идентификатор связи
    character = models.ForeignKey(Character, on_delete=models.CASCADE)  # Связь с персонажем
    quest = models.ForeignKey(Quest, related_name="character_quests", on_delete=models.CASCADE)  # Связь с квестом
    status = models.CharField(max_length=50)  # Статус выполнения квеста (например, "в процессе" или "завершен")
    started_at = models.DateTimeField(auto_now_add=True)  # Дата начала выполнения квеста
    completed_at = models.DateTimeField(null=True, blank=True)  # Дата завершения квеста (может быть пустым)

    def __str__(self):
        return f'{self.character.name} - {self.quest.name}'  # Строковое представление связи (персонаж - квест)
