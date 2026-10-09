from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('nutrition/', views.NutritionListView.as_view(), name='nutrition_list'),
]