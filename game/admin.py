from django.contrib import admin 
from .models import Player,Character,Item,Quest,CharacterItem,CharacterQuest 

class CharacterItemInline(admin.TabularInline):
    model = CharacterItem
    extra = 1


class CharacterQuestInline(admin.TabularInline):
    model = CharacterQuest
    extra = 1

class PlayerAdmin (admin.ModelAdmin):
    list_display = ["user_id","username","email","created_at","last_login"]
    list_display_links = ["user_id","username"]
    date_hierarchy = "created_at"
    search_fields = ["username","email"]
    

class CharacterAdmin (admin.ModelAdmin):
    readonly_fields = ["created_at","character_id"]
    list_display = ["character_id","user","name","level","created_at"]
    list_filter = ["level"]
    list_display_links = ["character_id","name"]
    date_hierarchy = "created_at"
    search_fields = ["name"]
    inlines = [CharacterItemInline, CharacterQuestInline]


class ItemAdmin (admin.ModelAdmin):
    readonly_fields = ["item_id"]
    list_display = ["item_id","name","rarity","value","character_items_count"]
    list_filter = ["rarity"]
    list_display_links = ["item_id","name"]
    search_fields = ["name"]

    @admin.display(description='Character Items Count')
    def character_items_count(self, obj):
        return obj.character_items.count()

class QuestAdmin (admin.ModelAdmin):
    readonly_fields = ["created_at","quest_id"]
    list_display = ["quest_id","name","difficulty","reward","character_quests_count"]
    list_filter = ["difficulty"]
    list_display_links = ["quest_id","name"]
    date_hierarchy = "created_at"
    search_fields = ["name"]

    @admin.display(description='Character Quest Count')
    def character_quests_count(self, obj):
        return obj.character_quests.count()

class CharacterItemAdmin (admin.ModelAdmin):
    readonly_fields = ["character_item_id", "acquired_at"]
    list_display = ["character_item_id","character_id","item_id","quantity","equipped"]
    list_filter = ["character_id","item_id","equipped"]
    list_display_links = ["character_item_id","character_id","item_id"]
    date_hierarchy = "acquired_at"
    # raw_id_fields = ["character", "item"]



class CharacterQuestAdmin (admin.ModelAdmin):
    readonly_fields = ["character_quest_id", "started_at"]
    list_display = ["character_quest_id","character_id","quest_id","started_at","status","completed_at"]
    list_filter = ["character_id","quest_id","status"]
    list_display_links = ["character_quest_id","character_id","quest_id"]
    date_hierarchy = "completed_at"
    raw_id_fields = ["character", "quest"]


admin.site.register(Player, PlayerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(CharacterItem, CharacterItemAdmin)
admin.site.register(CharacterQuest, CharacterQuestAdmin)
