from django.contrib import admin

from .models import Creature

@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
