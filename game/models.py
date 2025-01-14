from django.db import models  # Импортируем модуль для работы с моделями Django
from django.contrib.auth.models import AbstractUser  # Импортируем абстрактную модель пользователя
from django.core.exceptions import ValidationError  # Импортируем исключение для валидации
from simple_history.models import HistoricalRecords
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

class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название класса (например, "Warrior")
    description = models.TextField(blank=True, null=True)  # Описание класса, может быть пустым
    base_health = models.IntegerField(default=100)  # Базовый уровень здоровья для класса
    base_mana = models.IntegerField(default=50)  # Базовый уровень маны для класса

    def __str__(self):
        return self.name  # Возвращаем имя класса для строкового представления


# Модель для представления персонажей
class Character(models.Model):
    character_id = models.AutoField(primary_key=True)  # Уникальный идентификатор персонажа
    user = models.ForeignKey(Player, on_delete=models.CASCADE)  # Обязательная связь с пользователем
    name = models.CharField(max_length=50)  # Имя персонажа
    level = models.IntegerField(default=1)  # Уровень персонажа, начальное значение — 1
    experience = models.IntegerField()  # Опыт персонажа
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)  # Класс персонажа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания персонажа
    history = HistoricalRecords()  # История изменений

    def __str__(self):
        return f"{self.name} ({self.character_class.name})"  # Строковое представление персонажа (имя и класс)

    def clean(self):
        super().clean()  # Вызываем родительский метод clean()
        
        # Проверяем, что поле user уже установлено
        if not self.user_id:  # Используем `user_id`, чтобы избежать обращения к объекту
            return  # Если пользователь ещё не установлен, не проводим дальнейших проверок

        # Проверка, что уровень персонажа находится в пределах от 1 до 100
        if not (1 <= self.level <= 100):
            raise ValidationError("Level must be in range from 1 to 100.")

        # Проверка, что имя персонажа уникально для данного пользователя,
        # исключая текущего персонажа из проверки
        if self.character_id:
            # Если это редактирование существующего персонажа, исключаем его из проверки
            if Character.objects.filter(user=self.user, name=self.name).exclude(character_id=self.character_id).exists():
                raise ValidationError("Character with same name already exists.")
        else:
            # Если это новый персонаж, то проверка на уникальность
            if Character.objects.filter(user=self.user, name=self.name).exists():
                raise ValidationError("Character with same name already exists.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Запускаем полную валидацию перед сохранением объекта
        super().save(*args, **kwargs)  # Вызываем метод save() родительского класса

# Модель для представления предметов
class Item(models.Model):
    RARITY_CHOICES = [
        ('Common', 'Common'),
        ('Uncommon', 'Uncommon'),
        ('Rare', 'Rare'),
        ('Epic', 'Epic'),
        ('Legendary', 'Legendary'),
    ]
    
    item_id = models.AutoField(primary_key=True)  # Уникальный идентификатор предмета
    name = models.CharField(max_length=100)  # Название предмета
    description = models.TextField()  # Описание предмета
    type = models.CharField(max_length=50)  # Тип предмета (например, оружие, броня и т.д.)
    rarity = models.CharField(max_length=50, choices=RARITY_CHOICES)  # Редкость предмета
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
            raise ValidationError("Quantity of item must be more than 0.")

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
