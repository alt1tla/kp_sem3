from django.urls import path 
from . import views

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
]
