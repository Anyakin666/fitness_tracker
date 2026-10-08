from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkoutListView.as_view(), name='workout_list'),
]