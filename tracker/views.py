from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Workout, NutritionEntry, Measurement


class WorkoutListView(ListView):
    model = Workout #джанго сам делает Workout.objects.all()
    template_name = 'tracker/workout_list.html' #какой шаблон рендерить
    context_object_name = 'workouts' #как переменная буд. наз. в шаблоне


class NutritionListView(ListView):
    model = NutritionEntry
    template_name = 'tracker/nutrition_list.html'
    context_object_name = 'entries'


class MeasurementListView(ListView):
    model = Measurement
    template_name = 'tracker/measurement_list.html'
    context_object_name = 'measurements'