from django.contrib import admin
from .models import Fridge, Item

class FridgeItemInline(admin.TabularInline):
    model = Item
    extra = 0

class FridgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    inlines = [FridgeItemInline]

admin.site.register(Fridge, FridgeAdmin)
admin.site.register(Item)
