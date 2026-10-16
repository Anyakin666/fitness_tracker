from django import forms
from django.utils import timezone
from .models import Workout, NutritionEntry, Measurement


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'title', 'duration_minutes', 'notes']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'},  # HTML5-календарь
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        self.fields['date'].input_formats = ['%Y-%m-%d']


class NutritionForm(forms.ModelForm):
    class Meta:
        model = NutritionEntry
        fields = ['date', 'calories', 'protein', 'fat', 'carbs'] 
        widgets = {
                    'date': forms.DateInput(
                        format='%Y-%m-%d',
                        attrs={'type': 'date'},  # HTML5-календарь
                    ),
                }
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['date'].initial = timezone.now().date()
                self.fields['date'].input_formats = ['%Y-%m-%d']


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['date', 'weight', 'waist', 'hips', 'chest', 'thigh', 'biceps', 'calf']
        widgets = {
                    'date': forms.DateInput(
                        format='%Y-%m-%d',
                        attrs={'type': 'date'},  # HTML5-календарь
                        ),
                    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        self.fields['date'].input_formats = ['%Y-%m-%d']