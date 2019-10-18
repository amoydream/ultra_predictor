from django.contrib import admin
from . import models


class RaceInline(admin.TabularInline):
    model = models.Race


class RaceGroupAdmin(admin.ModelAdmin):
    inlines = [RaceInline]


admin.site.register(models.RaceGroup, RaceGroupAdmin)
