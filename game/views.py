from django.shortcuts import get_object_or_404, render, redirect 
from django.http import HttpResponse 
from rest_framework import viewsets
from django.http import Http404
from django.urls import reverse_lazy 
from game.models import Item, Quest, Player, Character, CharacterItem, CharacterQuest, CharacterClass
from game.permissions import IsSuperUserOrReadOnly
from .serializers import CharacterSerializer, CharacterClassSerializer, ItemSerializer, PlayerSerializer, QuestSerializer
from .forms import * 
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.views.generic.edit import FormView, DeleteView

class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def index(request):
    quests = Quest.objects.all()
    items = Item.objects.all()
    context = {"quests":quests,"items":items}
    return render(request,"index.html",context)

def item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        context = {"item":item}
    except Item.DoesNotExist:
        raise Http404("Item does not exist")
    return render(request,"item.html",context)

@login_required
def profile(request):
    user_id = request.user.user_id
    characters = Character.objects.filter(user=user_id)
    context = {"characters": characters}
    return render(request, "profile.html", context)

@login_required
def create_character(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user  # Привязываем персонажа к текущему пользователю
            character.level = 1  # Устанавливаем уровень 1
            character.experience = 0  # Устанавливаем опыт 0
            character.save()  # Сохраняем персонажа
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = CharacterForm()

    return render(request, "create_character.html", {'form': form})

@login_required
def character_detail(request, character_id):
    character = get_object_or_404(Character, character_id=character_id)
    inventory = CharacterItem.objects.filter(character=character)
    quests = CharacterQuest.objects.filter(character=character)
    available_quests = Quest.objects.exclude(character_quests__character=character)
    return render(request, "character.html", {'character': character, 'inventory': inventory, 'quests': quests, 'available_quests': available_quests})

def take_quest(request, quest_id):
    if request.method == "POST":
        quest = get_object_or_404(Quest, quest_id=quest_id)
        
        # Use filter to avoid MultipleObjectsReturned error
        characters = Character.objects.filter(user=request.user)
        if characters.exists():
            character = characters.first()  # Get the first character
        else:
            # Handle the case where no character is found
            return redirect('error_page')  # Redirect to an error page or show a message

        # Create a new CharacterQuest entry
        CharacterQuest.objects.create(
            character=character,
            quest=quest,
            status='pending'
        )

        return redirect('character_detail', character_id=character.character_id)

class DeleteUser(DeleteView):
    model = Player
    template_name = 'delete_user_confirm.html'
    success_url = reverse_lazy("index")

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance= request.user)
    return render(request, "edit_profile.html", {'form':form})

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsSuperUserOrReadOnly]

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [IsSuperUserOrReadOnly]

class CharacterClassViewSet(viewsets.ModelViewSet):
    queryset = CharacterClass.objects.all()
    serializer_class = CharacterClassSerializer
    permission_classes = [IsSuperUserOrReadOnly]
