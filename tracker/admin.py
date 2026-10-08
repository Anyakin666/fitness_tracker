from django.contrib import admin

# Register your models here.
from .models import Workout, NutritionEntry, Measurement

admin.site.register(Workout)
admin.site.register(NutritionEntry)
admin.site.register(Measurement)