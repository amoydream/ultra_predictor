from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from . import models
from .tasks import process_itra_download, process_endu_download, process_csv_files, process_csv_file_for_all


class PredictionRaceInline(admin.TabularInline):
    model = models.PredictionRace
    

class PredictionRaceResultsAdmin(admin.ModelAdmin):
    model = models.PredictionRaceResult


class HistoricalRaceResultsAdmin(admin.ModelAdmin):
    model = models.HistoricalRaceResult


class HistoricalRaceAdmin(admin.ModelAdmin):
    model = models.HistoricalRace


class PredictionRaceGroupAdmin(admin.ModelAdmin):
    change_list_template = "entities/race_group_changelist.html"
    inlines = [PredictionRaceInline]
    actions = [("generate_csv_for_group")]

    def generate_csv_for_group(self, request, queryset):
        for group in queryset:
            process_csv_files.delay(group.id)

    generate_csv_for_group.short_description = "Generate CSV file for predictions"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("global_csv/", self.global_csv)]
        return my_urls + urls

    def global_csv(self, request):
        process_csv_file_for_all.delay()
        self.message_user(request, "Send request to genereate CSV FILE")
        return HttpResponseRedirect("../")


class RunnerAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "itra_id"
      
    )
    inlines = [PredictionRaceInline]


class PredictionRaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "race_date",
        "distance",
        "ascent",
        "descent",
        "itra_point",
        "refreshment_points",
        "max_time",
        "country_start",
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
