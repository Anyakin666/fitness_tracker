from django import forms
from django.utils import timezone
from .models import Workout, NutritionEntry, Measurement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = 'До 150 символов. Буквы, цифры и @/./+/-/_'
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = 'Минимум 8 символов, не только цифры.'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text = 'Введите тот же пароль ещё раз.'

    class Meta:
        model = User
        fields = ('username',)