from django.shortcuts import get_object_or_404, render, redirect 
from django.http import HttpResponse 
from rest_framework import viewsets
from django.http import Http404
from django.urls import reverse_lazy 
from game.models import Item, Quest, Player, Character, CharacterItem, CharacterQuest, CharacterClass
from game.permissions import IsSuperUserOrReadOnly
from .serializers import CharacterSerializer, CharacterClassSerializer, ItemSerializer, PlayerSerializer, QuestSerializer
from .forms import * 
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.views.generic.edit import FormView, DeleteView
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator

# Главная страница с перечнем квестов и предметов
def index(request):
    quests = Quest.objects.all()  # Получаем все квесты
    items = Item.objects.all()  # Получаем все предметы
    context = {"quests": quests, "items": items}  # Контекст для передачи в шаблон
    return render(request, "index.html", context)  # Рендерим шаблон главной страницы

# Страница с подробной информацией о предмете
def item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)  # Получаем объект по ID
        context = {"item": item}  # Контекст для передачи в шаблон
    except Item.DoesNotExist:
        raise Http404("Item does not exist")  # Если предмет не найден, выбрасываем ошибку
    return render(request, "item.html", context)  # Рендерим шаблон страницы предмета

# Страница профиля пользователя
@login_required
def profile(request):
    user_id = request.user.user_id  # Получаем ID текущего пользователя
    characters = Character.objects.filter(user=user_id)  # Получаем персонажей текущего пользователя
    context = {"characters": characters}  # Контекст для передачи в шаблон
    return render(request, "profile.html", context)  # Рендерим шаблон страницы профиля

# Страница создания персонажа
@login_required
def create_character(request):
    if request.method == "POST":  # Обрабатываем POST-запрос
        form = CharacterForm(request.POST)
        if form.is_valid():  # Если форма валидна
            character = form.save(commit=False)  # Сохраняем объект, но не отправляем в базу
            character.user = request.user  # Связываем персонажа с текущим пользователем
            if character.level is None:  # Если уровень не указан
                character.level = 1  # Устанавливаем начальный уровень
            character.experience = 0  # Начальный опыт
            character.save()  # Сохраняем объект в базу данных
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = CharacterForm()  # Создаем пустую форму
    return render(request, "create_character.html", {"form": form})  # Рендерим страницу создания персонажа

# Страница с детальной информацией о персонаже
@login_required
def character_detail(request, character_id):
    character = get_object_or_404(Character, character_id=character_id)  # Получаем персонажа по ID или 404, если не найден
    inventory = CharacterItem.objects.filter(character=character)  # Получаем инвентарь персонажа
    quests = CharacterQuest.objects.filter(character=character)  # Получаем квесты персонажа

    # Фильтруем доступные квесты, исключая те, которые уже были приняты этим персонажем
    available_quests = Quest.objects.exclude(
        character_quests__character=character  # Исключаем уже принятые квесты
    ).exclude(
        character_quests__status='completed'  # Исключаем завершённые квесты
    )

    # Пагинация для доступных квестов (3 на страницу)
    paginator = Paginator(available_quests, 1)  # 3 квеста на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из URL
    page_obj = paginator.get_page(page_number)  # Получаем страницу

    return render(request, "character.html", {
        'character': character, 
        'inventory': inventory, 
        'quests': quests, 
        'page_obj': page_obj  # Передаем объект пагинации в шаблон
    })  # Рендерим шаблон

# Функция для принятия квеста персонажем
def take_quest(request, quest_id, character_id):
    if request.method == "POST":
        quest = get_object_or_404(Quest, quest_id=quest_id)  # Получаем квест по ID
        character = get_object_or_404(Character, character_id=character_id, user=request.user)  # Получаем персонажа по ID и пользователю

        # Создаем запись о том, что персонаж взял квест
        CharacterQuest.objects.create(
            character=character,
            quest=quest,
            status='pending'  # Статус квеста "ожидает выполнения"
        )
        return redirect('character_detail', character_id=character.character_id)  # Перенаправляем на страницу персонажа

# Отрисовка предметов с фильтрацией
def explore_items(request):
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')  # Получаем параметр для фильтрации по типу

    # Фильтруем предметы по названию, если задан поисковый запрос
    item_list = Item.objects.filter(name__icontains=search_query) if search_query else Item.objects.all()

    # Фильтрация по типу
    if type_filter:
        item_list = item_list.filter(type=type_filter)

    # Пагинация
    paginator = Paginator(item_list, 5)  # Показывать по 5 предметов на странице
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    return render(request, 'items.html', {'items': items, 'search_query': search_query, 'type_filter': type_filter})

# Отрисовка квестовой книги с фильтрацией
def quest_book(request):
    # Получаем параметры фильтрации из GET запроса
    difficulty_filter = request.GET.get('difficulty', '')
    date_from_filter = request.GET.get('date_from', '')
    date_to_filter = request.GET.get('date_to', '')
    
    # Начинаем с получения всех квестов
    quest_list = Quest.objects.all()

    # Фильтрация по сложности
    if difficulty_filter:
        quest_list = quest_list.filter(difficulty=difficulty_filter)
    
    # Фильтрация по диапазону дат (если указаны)
    if date_from_filter:
        date_from = datetime.strptime(date_from_filter, "%Y-%m-%d")
        quest_list = quest_list.filter(created_at__gte=date_from)
    
    if date_to_filter:
        date_to = datetime.strptime(date_to_filter, "%Y-%m-%d")
        quest_list = quest_list.filter(created_at__lte=date_to)

    # Фильтрация для текущего аутентифицированного пользователя
    if request.user.is_authenticated:
        quest_list = quest_list.filter(character_quests__character__user=request.user)

    # Пагинация
    paginator = Paginator(quest_list, 3)  # Показывать по 3 квестов на странице
    page_number = request.GET.get('page')
    quests = paginator.get_page(page_number)

    return render(request, 'quests.html', {
        'quests': quests,
        'difficulty_filter': difficulty_filter,
        'date_from_filter': date_from_filter,
        'date_to_filter': date_to_filter,
    })

# Страница редактирования профиля
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)  # Создаем форму с данными пользователя
        if form.is_valid():  # Проверяем, что форма валидна
            form.save()  # Сохраняем изменения
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = EditProfileForm(instance=request.user)  # Если GET-запрос, показываем текущие данные пользователя
    return render(request, "edit_profile.html", {'form': form})  # Рендерим форму редактирования профиля

# Сложный запрос для фильтрации квестов
def complex_query_1(request):
    character_id = request.GET.get("character_id")  # Получаем ID персонажа из запроса
    if not character_id:  # Проверяем, что ID указан
        return HttpResponse("Enter character ID.", status=400)
    
    # Запрос для сложных и невозможных квестов, не связанных с данным персонажем
    quests = Quest.objects.filter(
        (Q(difficulty="hard") | Q(difficulty="impossible")) &  # Сложность "Hard" или "Impossible"
        ~Q(character_quests__character_id=character_id)  # Исключаем уже связанные квесты
    )
    
    return render(request, "complex_query_1.html", {"quests": quests})  # Рендерим результат

# Сложный запрос для фильтрации персонажей
def complex_query_2(request):
    rarity_exclude = "legendary"  # Исключаем редкость
    characters = Character.objects.filter(
        (Q(characteritem__item__type="weapon") | Q(characteritem__item__type="armor")) &  # Предметы типа "weapon" или "armor"
        ~Q(characteritem__item__rarity=rarity_exclude)  # Исключаем редкость "legendary"
    ).distinct()  # Убираем дубли персонажей
    
    return render(request, "complex_query_2.html", {"characters": characters})  # Рендерим результат

# Отрисовка пагинации на API 
def pagination(request):
    return render(request, 'pagination.html') # Рендер результата

# Класс для регистрации нового пользователя
class RegistrationView(FormView):
    form_class = RegistrationForm  # Указываем форму для регистрации
    template_name = 'registration/registration.html'  # Шаблон для отображения страницы
    success_url = reverse_lazy("profile")  # Перенаправление на профиль после успешной регистрации

    def form_valid(self, form):
        form.save()  # Сохраняем нового пользователя
        return super().form_valid(form)  # Перенаправляем на страницу профиля

# Класс для удаления пользователя
class DeleteUser(DeleteView):
    model = Player  # Указываем модель пользователя
    template_name = 'delete_user_confirm.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy("index")  # Перенаправление на главную страницу после удаления

# Класс пагинации вывода персонажей 
class Pagination(PageNumberPagination):
    page_size = 1  # Установите количество элементов на странице
    page_size_query_param = 'page_size'  # Позволяет пользователю переопределять размер страницы через параметр
    max_page_size = 20  # Максимальный размер страницы

# ViewSet для работы с персонажами через API
class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()  # Получаем все персонажи
    serializer_class = CharacterSerializer  # Указываем сериализатор для персонажей
    permission_classes = [IsSuperUserOrReadOnly]  # Разрешения: только суперпользователь может изменять данные
    pagination_class = Pagination # Пагинация

# ViewSet для работы с предметами через API
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()  # Получаем все предметы
    serializer_class = ItemSerializer  # Указываем сериализатор для предметов
    permission_classes = [IsSuperUserOrReadOnly]  # Разрешения: только суперпользователь может изменять данные
    pagination_class = Pagination # Пагинация

# ViewSet для работы с квестами через API
class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()  # Получаем все квесты
    serializer_class = QuestSerializer  # Указываем сериализатор для квестов
    permission_classes = [IsSuperUserOrReadOnly]  # Разрешения: только суперпользователь может изменять данные
    pagination_class = Pagination # Пагинация

# ViewSet для работы с классами персонажей через API
class CharacterClassViewSet(viewsets.ModelViewSet):
    queryset = CharacterClass.objects.all()  # Получаем все классы персонажей
    serializer_class = CharacterClassSerializer  # Указываем сериализатор для классов персонажей
    permission_classes = [IsSuperUserOrReadOnly]  # Разрешения: только суперпользователь может изменять данные
    pagination_class = Pagination # Пагинация

#? Нужен ли API для пользовательских аккаунтов
# ViewSet для работы с игроками через API
# class PlayerViewSet(viewsets.ModelViewSet):
#     queryset = Player.objects.all()  # Получаем всех игроков
#     serializer_class = PlayerSerializer  # Указываем сериализатор для игроков
#     permission_classes = [IsSuperUserOrReadOnly]  # Разрешения: только суперпользователь может изменять данные
