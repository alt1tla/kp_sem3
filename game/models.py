from django.db import models 
from django.contrib.auth.models import AbstractUser

# Модель для представления игроков (пользователей)
class Player(AbstractUser):
    user_id = models.AutoField(primary_key=True)  # Уникальный идентификатор пользователя
    username = models.CharField(max_length=50, unique=True)  # Имя пользователя (уникальное)
    email = models.EmailField(max_length=100)  # Email адрес
    password = models.CharField(max_length=100)  # Пароль
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания пользователя
    last_login = models.DateTimeField(null=True, blank=True)  # Дата и время последнего входа

    USERNAME_FIELD = 'username'  # Поле, используемое для входа
    REQUIRED_FIELDS = ['email']  # Обязательные поля при создании пользователя

    def __str__(self):
        return self.username  # Представление объекта в виде строки (имя пользователя)

# Модель для представления классов персонажей
class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название класса, например, "Воин"
    description = models.TextField(blank=True, null=True)  # Описание класса (может быть пустым)
    base_health = models.IntegerField(default=100)  # Базовый уровень здоровья
    base_mana = models.IntegerField(default=50)  # Базовый уровень маны

# Модель для представления персонажей
class Character(models.Model):
    character_id = models.AutoField(primary_key=True)  # Уникальный идентификатор персонажа
    user = models.ForeignKey(Player, on_delete=models.CASCADE)  # Связь с пользователем (владелец персонажа)
    name = models.CharField(max_length=50)  # Имя персонажа
    level = models.IntegerField()  # Уровень персонажа
    experience = models.IntegerField()  # Опыт персонажа
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)  # Связь с классом персонажа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания персонажа

    def __str__(self):
        return f"{self.name} ({self.character_class.name})"  # Представление объекта в виде строки (имя и класс)

# Модель для представления предметов
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)  # Уникальный идентификатор предмета
    name = models.CharField(max_length=100)  # Название предмета
    description = models.TextField()  # Описание предмета
    type = models.CharField(max_length=50)  # Тип предмета
    rarity = models.CharField(max_length=50)  # Редкость предмета
    value = models.IntegerField()  # Ценность предмета (например, в деньгах или очках)

    def __str__(self):
        return self.name  # Представление объекта в виде строки (название предмета)

# Модель для связи предметов с персонажами (инвентарь)
class CharacterItem(models.Model):
    character_item_id = models.AutoField(primary_key=True)  # Уникальный идентификатор
    character = models.ForeignKey(Character, on_delete=models.CASCADE)  # Связь с персонажем
    item = models.ForeignKey(Item, related_name='character_items', on_delete=models.CASCADE)  # Связь с предметом
    quantity = models.IntegerField()  # Количество предметов
    equipped = models.BooleanField(default=False)  # Флаг, указывает, экипирован ли предмет
    acquired_at = models.DateTimeField(auto_now_add=True)  # Дата и время получения предмета

    def __str__(self):
        return f'{self.character.name} - {self.item.name}'  # Представление объекта в виде строки (персонаж - предмет)

# Модель для представления квестов
class Quest(models.Model):
    quest_id = models.AutoField(primary_key=True)  # Уникальный идентификатор квеста
    name = models.CharField(max_length=100)  # Название квеста
    description = models.TextField()  # Описание квеста
    reward = models.CharField(max_length=100)  # Награда за выполнение квеста
    difficulty = models.CharField(max_length=50)  # Сложность квеста
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания квеста

    def __str__(self):
        return self.name  # Представление объекта в виде строки (название квеста)

# Модель для связи персонажей с квестами (задания персонажей)
class CharacterQuest(models.Model):
    character_quest_id = models.AutoField(primary_key=True)  # Уникальный идентификатор
    character = models.ForeignKey(Character, on_delete=models.CASCADE)  # Связь с персонажем
    quest = models.ForeignKey(Quest, related_name="character_quests", on_delete=models.CASCADE)  # Связь с квестом
    status = models.CharField(max_length=50)  # Статус выполнения квеста (например, "в процессе" или "завершен")
    started_at = models.DateTimeField(auto_now_add=True)  # Дата и время начала квеста
    completed_at = models.DateTimeField(null=True, blank=True)  # Дата и время завершения квеста (может быть пустым)

    def __str__(self):
        return f'{self.character.name} - {self.quest.name}'  # Представление объекта в виде строки (персонаж - квест)
