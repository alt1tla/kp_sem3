from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet, CharacterClassViewSet, PlayerViewSet, ItemViewSet, QuestViewSet
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Game API",
        default_version='v1',
        description="API для RPG игры",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@gameapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Swagger доступен для всех
)

router = DefaultRouter()
router.register(r'characters', CharacterViewSet)
router.register(r'character-classes', CharacterClassViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'items', ItemViewSet)
router.register(r'quests', QuestViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<int:item_id>/", views.item, name="item"),
    path("accounts/profile/", views.profile, name="profile"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("delete_user/<int:pk>/", views.DeleteUser.as_view(), name="delete_user"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('create_character/', views.create_character, name='create_character'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path('quest/take/<int:quest_id>/', views.take_quest, name='take_quest'),
    path("api/", include(router.urls)),  # Подключаем маршруты роутера
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]
