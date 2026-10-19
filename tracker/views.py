from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Workout, NutritionEntry, Measurement
from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone

from django.urls import reverse_lazy
from .forms import WorkoutForm, NutritionForm, MeasurementForm
from django.contrib.auth.decorators import login_required


class WorkoutCreateView(CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'tracker/workout_form.html'
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NutritionCreateView(CreateView):
    model = NutritionEntry
    form_class = NutritionForm
    template_name = 'tracker/nutrition_form.html'
    success_url = reverse_lazy('nutrition_list')

    def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)
    


class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'tracker/measurement_form.html'
    success_url = reverse_lazy('measurement_list')

    def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)
    


class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'tracker/workout_form.html'
    success_url = reverse_lazy('workout_list')    


class WorkoutDeleteView(DeleteView):
    model = Workout
    template_name = 'tracker/workout_confirm_delete.html'
    success_url = reverse_lazy('workout_list')    


class MeasurementUpdateView(UpdateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'tracker/measurement_form.html'
    success_url = reverse_lazy('measurement_list')    


class MeasurementDeleteView(DeleteView):
    model = Measurement
    template_name = 'tracker/measurement_confirm_delete.html'
    success_url = reverse_lazy('measurement_list')    


class NutritionUpdateView(UpdateView):
    model = NutritionEntry
    form_class = NutritionForm
    template_name = 'tracker/nutrition_form.html'
    success_url = reverse_lazy('nutrition_list')

class NutritionDeleteView(DeleteView):
    model = NutritionEntry
    template_name = 'tracker/nutrition_confirm_delete.html'
    success_url = reverse_lazy('nutrition_list')




class WorkoutListView(ListView):
    model = Workout #джанго сам делает Workout.objects.all()
    template_name = 'tracker/workout_list.html' #какой шаблон рендерить
    context_object_name = 'workouts' #как переменная буд. наз. в шаблоне

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class NutritionListView(ListView):
    model = NutritionEntry
    template_name = 'tracker/nutrition_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class MeasurementListView(ListView):
    model = Measurement
    template_name = 'tracker/measurement_list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@login_required
def index(request):
    last_workout = Workout.objects.filter(user=request.user).first()
    last_measurement = Measurement.objects.filter(user=request.user).first()
    week_ago = timezone.now().date() - timedelta(days=7)
    week_entries = NutritionEntry.objects.filter(user=request.user, date__gte=week_ago)
    avg_calories = week_entries.aggregate(Avg('calories'))['calories__avg']
    return render(request, 'index.html', context={
        'last_workout' : last_workout,
        'last_measurement' : last_measurement,
        'avg_calories': avg_calories,
    }) 