from django.shortcuts import render

from django.views.generic import ListView, DetailView


from .models import PredictionRaceGroup, PredictionRaceResult


class PredictionRaceGroupListView(ListView):
    model = PredictionRaceGroup
    context_object_name = "prediction_race_groups_list"
    queryset = (
        PredictionRaceGroup.objects.all()
        .prefetch_related("prediction_races")
        .prefetch_related("prediction_races__prediction_race_results")
    )


class PredictionRaceResultGroupListView(DetailView):
    model = PredictionRaceGroup
    context_object_name = "prediction_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "group_race_results"
        ] = self.get_object().all_results_of_prediction_races()
        return context

