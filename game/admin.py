from django.contrib import admin 
from .models import Player, Character, Item, Quest, CharacterItem, CharacterQuest  
from import_export import resources
from django.db.models import Count
from import_export.admin import ImportExportModelAdmin


class CharacterItemInline(admin.TabularInline):
    model = CharacterItem
    extra = 1


class CharacterQuestInline(admin.TabularInline):
    model = CharacterQuest
    extra = 1


class PlayerAdmin (admin.ModelAdmin):
    list_display = ["user_id", "username", "email", "created_at", "last_login"]
    list_display_links = ["user_id", "username"]
    date_hierarchy = "created_at"
    search_fields = ["username", "email"]


class CharacterResource(resources.ModelResource):
    # Добавляем новые поля для экспорта
    item_count = resources.Field()
    completed_quests_count = resources.Field()
    in_progress_quests_count = resources.Field()
    # Дополнительное поле для вывода описания класса
    character_class_description = resources.Field()

    class Meta:
        model = Character
        fields = ('character_id', 'user__username', 'name', 
                  'level', 'experience', 'character_class', 'character_class_description',  
                  'created_at', 'item_count', 'completed_quests_count', 
                  'in_progress_quests_count',)  # Укажите поля, которые нужно экспортировать
        export_order = ('character_id', 'user__username', 'name', 'character_class',
                        'character_class_description',   'level', 'experience',
                        'item_count', 'completed_quests_count',
                        'in_progress_quests_count', 'created_at')  # Порядок для экспорта
    # Этот метод будет использоваться для извлечения имени класса персонажа вместо ID
    def dehydrate_character_class(self, character):
        # Возвращаем имя класса персонажа, а не его ID
        return character.character_class.name if character.character_class else ''
    # Метод для извлечения количества предметов у персонажа
    def dehydrate_item_count(self, character):
        return character.characteritem_set.aggregate(count=Count('item'))['count'] or 0
    # Метод для извлечения количества выполненных квестов у персонажа
    def dehydrate_completed_quests_count(self, character):
        return character.characterquest_set.filter(status="completed").count()
    # Метод для извлечения количества квестов в процессе у персонажа
    def dehydrate_in_progress_quests_count(self, character):
        return character.characterquest_set.filter(status="pending").count()


class CharacterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CharacterResource  # Подключаем ресурс
    readonly_fields = ["created_at", "character_id"]
    list_display = ["character_id", "user", "name", "level", "created_at"]
    list_filter = ["level"]
    list_display_links = ["character_id", "name"]
    date_hierarchy = "created_at"
    search_fields = ["name"]
    inlines = [CharacterItemInline, CharacterQuestInline]


class ItemResource(resources.ModelResource):
    character_items_count = resources.Field()  # Количество предметов у персонажей
    item_description = resources.Field()  # Описание предмета


    class Meta:
        model = Item
        fields = ('item_id', 'name', 'rarity', 'value', 'character_items_count')
        export_order = ('item_id', 'name', 'rarity', 'value', 'character_items_count')
      # Метод для подсчета количества предметов у персонажей
    def dehydrate_character_items_count(self, item):
        return item.character_items.count()  # Подсчитываем количество предметов у персонажей
    # Метод для кастомизации выборки данных для экспорта
    def get_export_queryset(self, queryset):
        # Применяем фильтрацию, чтобы выбрать только предметы с редкостью 'Rare'
        return queryset.filter(rarity='Rare')
    # Метод для кастомизации заголовков в экспортируемом файле
    def get_export_headers(self, *args, **kwargs):
        headers = super().get_export_headers(*args, **kwargs)
        # Пример: добавление префикса к заголовку
        headers[0] = 'ID'  # Пример: изменяем первый заголовок
        return headers



class ItemAdmin (ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ItemResource  # Подключаем ресурс
    readonly_fields = ["item_id"]
    list_display = ["item_id", "name", "rarity", "value", "character_items_count"]
    list_filter = ["rarity"]
    list_display_links = ["item_id", "name"]
    search_fields = ["name"]
    @admin.display(description='Character Items Count')
    def character_items_count(self, obj):
        return obj.character_items.count()


class QuestAdmin (admin.ModelAdmin):
    readonly_fields = ["created_at","quest_id"]
    list_display = ["quest_id", "name", "difficulty", "reward", "character_quests_count"]
    list_filter = ["difficulty"]
    list_display_links = ["quest_id", "name"]
    date_hierarchy = "created_at"
    search_fields = ["name"]
    @admin.display(description='Character Quest Count')
    def character_quests_count(self, obj):
        return obj.character_quests.count()


class CharacterItemAdmin (admin.ModelAdmin):
    readonly_fields = ["character_item_id", "acquired_at"]
    list_display = ["character_item_id", "character_id","item_id", "quantity","equipped"]
    list_filter = ["character_id", "item_id", "equipped"]
    list_display_links = ["character_item_id", "character_id", "item_id"]
    date_hierarchy = "acquired_at"
    # raw_id_fields = ["character", "item"]


class CharacterQuestAdmin (admin.ModelAdmin):
    readonly_fields = ["character_quest_id", "started_at"]
    list_display = ["character_quest_id", "character_id", "quest_id", "started_at", "status", "completed_at"]
    list_filter = ["character_id", "quest_id", "status"]
    list_display_links = ["character_quest_id", "character_id", "quest_id"]
    date_hierarchy = "completed_at"
    raw_id_fields = ["character", "quest"]


admin.site.register(Player, PlayerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(CharacterItem, CharacterItemAdmin)
admin.site.register(CharacterQuest, CharacterQuestAdmin)
