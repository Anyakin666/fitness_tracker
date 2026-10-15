from django import forms
from django.utils import timezone
from .models import Workout


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