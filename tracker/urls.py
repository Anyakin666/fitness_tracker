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
    path('workouts/<int:pk>/edit/', views.WorkoutUpdateView.as_view(), name='workout_edit'),
    path('workouts/<int:pk>/delete/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
    path('nutrition/<int:pk>/edit/', views.NutritionUpdateView.as_view(), name='nutrition_edit'),
    path('nutrition/<int:pk>/delete/', views.NutritionDeleteView.as_view(), name='nutrition_delete'),
    path('measurement/<int:pk>/edit/', views.MeasurementUpdateView.as_view(), name='measurement_edit'),
    path('measurement/<int:pk>/delete/', views.MeasurementDeleteView.as_view(), name='measurement_delete'),
]