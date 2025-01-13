from django.urls import path, include  # Импортируем необходимые модули для работы с маршрутами
from rest_framework.routers import DefaultRouter  # Импортируем DefaultRouter для автоматического создания маршрутов
from .views import CharacterViewSet, CharacterClassViewSet, ItemViewSet, QuestViewSet  # Импортируем viewset'ы для API
from . import views  # Импортируем обычные представления (views) для обработки веб-страниц
from rest_framework import permissions  # Импортируем разрешения для API
from drf_yasg.views import get_schema_view  # Импортируем метод для генерации Swagger документации
from drf_yasg import openapi  # Импортируем открытие API схемы

# Настройка Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Game API",  # Название API
        default_version='v1',  # Версия API
        description="API для RPG игры",  # Описание API
        terms_of_service="https://www.google.com/policies/terms/",  # Условия использования
        contact=openapi.Contact(email="veronika@gerdzhikova.ru"),  # Контактная информация
        license=openapi.License(name="BSD License"),  # Лицензия на API
    ),
    public=True,  # Указываем, что схема будет доступна для всех
    permission_classes=(permissions.AllowAny,),  # Разрешения для Swagger: доступен всем без ограничений
)

# Создаем роутер для автоматического создания маршрутов для API
router = DefaultRouter()
router.register(r'character-classes', CharacterClassViewSet)  # Маршрут для работы с классами персонажей
router.register(r'characters', CharacterViewSet)  # Маршрут для работы с персонажами
router.register(r'items', ItemViewSet)  # Маршрут для работы с предметами
router.register(r'quests', QuestViewSet)  # Маршрут для работы с квестами

#? Это для пользовательского API 
# router.register(r'players', PlayerViewSet)  # Маршрут для работы с игроками

# Определяем URL-пути для проекта
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Страница для отображения Swagger UI
    path("", views.index, name="index"),  # Главная страница (обрабатывает запросы на главную страницу)
    path("item/<int:item_id>/", views.item, name="item"),  # Страница с деталями предмета по его ID
    path("accounts/profile/", views.profile, name="profile"),  # Страница профиля пользователя
    path("registration/", views.RegistrationView.as_view(), name="registration"),  # Страница регистрации
    path("delete_user/<int:pk>/", views.DeleteUser.as_view(), name="delete_user"),  # Страница для удаления пользователя
    path("edit_profile/", views.edit_profile, name="edit_profile"),  # Страница для редактирования профиля пользователя
    path('create_character/', views.create_character, name='create_character'),  # Страница для создания персонажа
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),  # Страница с детальной информацией о персонаже
    path('take_quest/<int:quest_id>/<int:character_id>/', views.take_quest, name='take_quest'),  # Страница для принятия квеста персонажем
    path("api/", include(router.urls)),  # Подключаем маршруты для API через роутер
    path('pagination/', views.pagination, name='pagination'),  # Новый маршрут для HTML-шаблона
    path('complex_query_1/', views.complex_query_1, name='complex_query_1'),  # Страница для выполнения сложного запроса 1
    path('complex_query_2/', views.complex_query_2, name='complex_query_2'),  # Страница для выполнения сложного запроса 2
]
