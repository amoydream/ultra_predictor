from django.contrib import admin
from . import models


class PredictionRaceInline(admin.TabularInline):
    model = models.PredictionRace


class PredictionRaceGroupAdmin(admin.ModelAdmin):
    inlines = [PredictionRaceInline]


class PredictionRaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "distance",
        "elevation_gain",
        "elevation_lost",
        "itra",
        "food_point",
        "time_limit",
        "itra_download_status",
    )
    actions = [("make_race_ready")]

    def make_race_ready(self, request, queryset):
        queryset.update(itra_download_status="R")
    make_race_ready.short_description = "Download data from Itra Page"        


admin.site.register(models.PredictionRaceGroup, PredictionRaceGroupAdmin)
admin.site.register(models.PredictionRace, PredictionRaceAdmin)
