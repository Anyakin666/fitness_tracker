from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('nutrition/', views.NutritionListView.as_view(), name='nutrition_list'),
    path('measurement/', views.MeasurementListView.as_view(), name='measurement_list'),
    path('workouts/add/', views.WorkoutCreateView.as_view(), name='workout_add'),
    path('nutrition/add/', views.NutritionCreateView.as_view(), name='nutrition_add'),
    path('measurement/add/', views.MeasurementCreateView.as_view(), name='measurement_add'),
]