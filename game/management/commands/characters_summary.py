from django.core.management.base import BaseCommand
from game.models import Character  # Импортируем модель Character
from django.utils.timezone import now, localtime

class Command(BaseCommand):
    help = 'Выводит количество персонажей, созданных за сегодня'

    def handle(self, *args, **options):
        # Получаем текущую дату
        today = localtime(now()).date()

        # Считаем количество персонажей, созданных за сегодня
        characters_count = Character.objects.filter(created_at__date=today).count()

        # Выводим результат в консоль
        self.stdout.write(f'Количество персонажей, созданных сегодня ({today}): {characters_count}')
