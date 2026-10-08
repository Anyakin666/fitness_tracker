from django.contrib import admin

# Register your models here.
from .models import Workout, NutritionEntry, Measurement

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'duration_minutes')
    list_filter = ('title', 'date')
    search_fields = ('notes',)
admin.site.register(NutritionEntry)
admin.site.register(Measurement)