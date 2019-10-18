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
        "itra_download_status",
    )
    actions = [("make_race_ready")]

    def make_race_ready(self, request, queryset):
        queryset.update(itra_download_status="R")
    make_race_ready.short_description = "Download data from Itra Page"        


admin.site.register(models.RaceGroup, RaceGroupAdmin)
admin.site.register(models.Race, RaceAdmin)
