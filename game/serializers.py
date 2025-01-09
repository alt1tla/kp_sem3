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
        fields = ['character_id', 'user', 'name', 'level', 'experience', 'character_class', 'created_at']  # Перечисляем поля для сериализованного вывода

    def validate(self, data):
        # Проверка уникальности имени персонажа для данного пользователя
        user = data['user']  # Получаем пользователя из данных
        name = data['name']  # Получаем имя персонажа из данных
        # Проверяем, существует ли уже персонаж с таким именем у этого пользователя
        if Character.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError("Персонаж с таким именем уже существует у этого игрока.")
        
        # Проверка уровня персонажа (он должен быть в пределах от 1 до 100)
        level = data.get('level', 1)  # Если уровень не передан, используем 1 по умолчанию
        if not (1 <= level <= 100):
            raise serializers.ValidationError("Уровень персонажа должен быть в диапазоне от 1 до 100.")
        
        # Возвращаем обработанные данные
        return data

# Сериализатор для создания нового персонажа
class CharacterCreateSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(queryset=CharacterClass.objects.all())  # Ссылка на класс персонажа

    class Meta:
        model = Character  # Указываем модель для сериализатора
        fields = ['name', 'level', 'experience', 'character_class', 'user']  # Поля для сериализации при создании персонажа
