from django.test import TestCase
from datetime import datetime, timedelta
from .models import Character, Quest, CharacterQuest, Player

class CharacterQuestModelTests(TestCase):

    def setUp(self):
        # Создаем игрока 
        self.player = Player.objects.create(username='testuser', email='test@example.com', password='password')

        # Создаем персонажа 
        self.character = Character.objects.create(user=self.player, name='Test Character', level=1, experience=0)

        # Создаем задание 
        self.quest = Quest.objects.create(name='Test Quest', description='Test quest description', reward='Test reward', difficulty='Easy')

    def test_completed_at_cannot_be_before_started_at(self):
        # Создаем объект CharacterQuest с датой начала, равной текущему времени
        started_at = datetime.now()
        character_quest = CharacterQuest.objects.create(character=self.character, quest=self.quest, status='In Progress', started_at=started_at)

        # Пытаемся установить дату завершения раньше даты начала
        completed_at = started_at - timedelta(days=1)

        # Проверяем, что при попытке установить completed_at раньше started_at возникает ошибка IntegrityError
        with self.assertRaises(Exception):
            character_quest.completed_at = completed_at
            character_quest.save()

        # completed_at осталась None
        self.assertIsNone(character_quest.completed_at)

    def test_completed_at_can_be_equal_to_started_at(self):
        # Создаем объект CharacterQuest с датой начала, равной текущему времени
        started_at = datetime.now()
        character_quest = CharacterQuest.objects.create(character=self.character, quest=self.quest, status='In Progress', started_at=started_at)

        # Устанавливаем дату завершения равной дате начала
        character_quest.completed_at = started_at
        character_quest.save()

        # completed_at установлена верно
        self.assertEqual(character_quest.completed_at, started_at)

    def test_completed_at_can_be_after_started_at(self):
        # Создаем объект CharacterQuest с датой начала, равной текущему времени
        started_at = datetime.now()
        character_quest = CharacterQuest.objects.create(character=self.character, quest=self.quest, status='In Progress', started_at=started_at)

        # Устанавливаем дату завершения после даты начала
        completed_at = started_at + timedelta(days=1)
        character_quest.completed_at = completed_at
        character_quest.save()

        # Пcompleted_at установлена верно
        self.assertEqual(character_quest.completed_at, completed_at)
