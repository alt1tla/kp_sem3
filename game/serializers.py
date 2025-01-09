from rest_framework import serializers  # Импортируем модуль для создания сериализаторов
from .models import Character, CharacterClass, Player, Item, Quest  # Импортируем модели, с которыми будем работать

# Сериализатор для модели Player
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player  # Указываем модель, для которой создается сериализатор
        fields = ['user_id', 'username', 'email', 'created_at', 'last_login']  # Перечисляем поля, которые будут включены в сериализованный вывод

# Сериализатор для модели Item
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item  # Указываем модель, для которой создается сериализатор
        fields = ['item_id', 'name', 'description', 'type', 'rarity', 'value']  # Перечисляем поля, которые будут включены в сериализованный вывод

# Сериализатор для модели Quest
class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest  # Указываем модель, для которой создается сериализатор
        fields = ['quest_id', 'name', 'description', 'reward', 'difficulty', 'created_at']  # Перечисляем поля, которые будут включены в сериализованный вывод

# Сериализатор для модели CharacterClass
class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass  # Указываем модель, для которой создается сериализатор
        fields = ['id', 'name', 'description', 'base_health', 'base_mana']  # Перечисляем поля, которые будут включены в сериализованный вывод

# Сериализатор для модели Character с вложенным сериализатором для CharacterClass
class CharacterSerializer(serializers.ModelSerializer):
    character_class = CharacterClassSerializer()  # Вложенный сериализатор для класса персонажа

    class Meta:
        model = Character  # Указываем модель, для которой создается сериализатор
        fields = ['character_id', 'user', 'name', 'level', 'experience', 'character_class', 'created_at']  # Перечисляем поля, которые будут включены в сериализованный вывод
