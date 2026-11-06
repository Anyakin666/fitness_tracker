from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Workout, NutritionEntry, Measurement, UserProfile
from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone

from django.urls import reverse_lazy
from .forms import WorkoutForm, NutritionForm, MeasurementForm, SignUpForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tracker.utils import calculate_calories


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


@method_decorator(login_required, name='dispatch')
class WorkoutCreateView(CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'tracker/workout_form.html'
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NutritionCreateView(CreateView):
    model = NutritionEntry
    form_class = NutritionForm
    template_name = 'tracker/nutrition_form.html'
    success_url = reverse_lazy('nutrition_list')

    def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)
    

@method_decorator(login_required, name='dispatch')
class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'tracker/measurement_form.html'
    success_url = reverse_lazy('measurement_list')

    def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'tracker/userprofile_detail.html'

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user, 
            defaults={
                'goal': 'maintain',
                'gender': 'male',
                'age': 25,
                'height': 170,
                'weight': 70,
                'activity': 'moderate',
            }
        )
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calories'] = calculate_calories(self.object)
        return context


@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'tracker/userprofile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'goal': 'maintain',
                'gender': 'male',
                'age': 25,
                'height': 170,
                'weight': 70,
                'activity': 'moderate',
            }
        )
        return profile
    

@method_decorator(login_required, name='dispatch')
class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'tracker/workout_form.html'
    success_url = reverse_lazy('workout_list')    


@method_decorator(login_required, name='dispatch')
class WorkoutDeleteView(DeleteView):
    model = Workout
    template_name = 'tracker/workout_confirm_delete.html'
    success_url = reverse_lazy('workout_list')    


@method_decorator(login_required, name='dispatch')
class MeasurementUpdateView(UpdateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'tracker/measurement_form.html'
    success_url = reverse_lazy('measurement_list')    


@method_decorator(login_required, name='dispatch')
class MeasurementDeleteView(DeleteView):
    model = Measurement
    template_name = 'tracker/measurement_confirm_delete.html'
    success_url = reverse_lazy('measurement_list')    


@method_decorator(login_required, name='dispatch')
class NutritionUpdateView(UpdateView):
    model = NutritionEntry
    form_class = NutritionForm
    template_name = 'tracker/nutrition_form.html'
    success_url = reverse_lazy('nutrition_list')


@method_decorator(login_required, name='dispatch')
class NutritionDeleteView(DeleteView):
    model = NutritionEntry
    template_name = 'tracker/nutrition_confirm_delete.html'
    success_url = reverse_lazy('nutrition_list')


@method_decorator(login_required, name='dispatch')
class WorkoutListView(ListView):
    model = Workout #джанго сам делает Workout.objects.all()
    template_name = 'tracker/workout_list.html' #какой шаблон рендерить
    context_object_name = 'workouts' #как переменная буд. наз. в шаблоне

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class NutritionListView(ListView):
    model = NutritionEntry
    template_name = 'tracker/nutrition_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
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