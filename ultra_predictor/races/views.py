from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PredictionRaceGroup, PredictionRaceResult


class PredictionRaceGroupListView(LoginRequiredMixin, ListView):
    model = PredictionRaceGroup
    context_object_name = "prediction_race_groups_list"
    queryset = (
        PredictionRaceGroup.objects.all()
        .prefetch_related("prediction_races")
        .prefetch_related("prediction_races__prediction_race_results")
    )


class PredictionRaceResultGroupListView(
    LoginRequiredMixin, DetailView, MultipleObjectMixin
):
    model = PredictionRaceGroup
    context_object_name = "prediction_group"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        self.object_list = self.get_object().all_results_of_prediction_races()
        context = super().get_context_data(**kwargs)
        _, page, _, _ = self.paginate_queryset(self.object_list, self.paginate_by)
        context["group_race_results"] = page
        return context
