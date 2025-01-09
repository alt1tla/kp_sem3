from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

class Player(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Название класса, например, "Воин"
    description = models.TextField(blank=True, null=True)  # Описание класса (необязательно)
    base_health = models.IntegerField(default=100)  # Пример базового здоровья
    base_mana = models.IntegerField(default=50)  # Пример базовой маны

class Character(models.Model):
    character_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    experience = models.IntegerField()
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)  # Связь с CharacterClass
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.character_class.name})" 

    def __str__(self):
        return self.name


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50)
    rarity = models.CharField(max_length=50)
    value = models.IntegerField()

    def __str__(self):
        return self.name

class CharacterItem(models.Model):
    character_item_id = models.AutoField(primary_key=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='character_items', on_delete=models.CASCADE) # related
    quantity = models.IntegerField()
    equipped = models.BooleanField(default=False)
    acquired_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.character.name} - {self.item.name}'


class Quest(models.Model):
    quest_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class CharacterQuest(models.Model):
    character_quest_id = models.AutoField(primary_key=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, related_name="character_quests", on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.character.name} - {self.quest.name}'


