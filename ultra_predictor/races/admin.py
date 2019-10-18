from django.contrib import admin
from . import models


class RaceInline(admin.TabularInline):
    model = models.Race


class RaceGroupAdmin(admin.ModelAdmin):
    inlines = [RaceInline]


class RaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "distance",
        "elevation_gain",
        "elevation_lost",
        "itra",
        "food_point",
        "time_limit",
    )


admin.site.register(models.RaceGroup, RaceGroupAdmin)
admin.site.register(models.Race, RaceAdmin)
