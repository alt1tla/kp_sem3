from rest_framework import serializers
from .models import Character, CharacterClass, Player, Item, Quest

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['user_id', 'username', 'email', 'created_at', 'last_login']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'description', 'type', 'rarity', 'value']

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['quest_id', 'name', 'description', 'reward', 'difficulty', 'created_at']

class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ['id', 'name', 'description', 'base_health', 'base_mana']

class CharacterSerializer(serializers.ModelSerializer):
    character_class = CharacterClassSerializer()  # Вложенный сериализатор для класса персонажа

    class Meta:
        model = Character
        fields = ['character_id', 'user', 'name', 'level', 'experience', 'character_class', 'created_at']
