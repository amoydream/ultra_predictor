from django.contrib import admin
from . import models
from .tasks import process_itra_download, process_endu_download


class PredictionRaceInline(admin.TabularInline):
    model = models.PredictionRace


class PredictionRaceResultsAdmin(admin.ModelAdmin):
    model = models.PredictionRaceResult


class HistoricalRaceResultsAdmin(admin.ModelAdmin):
    model = models.HistoricalRaceResult


class HistoricalRaceAdmin(admin.ModelAdmin):
    model = models.HistoricalRace


class PredictionRaceGroupAdmin(admin.ModelAdmin):
    inlines = [PredictionRaceInline]


class RunnerAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
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
    actions = [("download_itra"), ("download_enduhub")]

    def download_itra(self, request, queryset):
        queryset.update(itra_download_status="R")
        for race in queryset:
            task = process_itra_download(race.id)
            task.delay()

    download_itra.short_description = "Download data from Itra Page"

    def download_enduhub(self, request, queryset):
        queryset.update(itra_download_status="R")
        for race in queryset:
            process_endu_download(race.id)
            

    download_enduhub.short_description = "Download data from Enduhub"


admin.site.register(models.PredictionRaceGroup, PredictionRaceGroupAdmin)
admin.site.register(models.Runner, RunnerAdmin)

admin.site.register(models.PredictionRace, PredictionRaceAdmin)
admin.site.register(models.PredictionRaceResult, PredictionRaceResultsAdmin)

admin.site.register(models.HistoricalRace, HistoricalRaceAdmin)
admin.site.register(models.HistoricalRaceResult, HistoricalRaceResultsAdmin)

admin.site.register(models.Event, EventAdmin)
