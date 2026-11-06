from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Workout(models.Model):
    class Title(models.TextChoices):
        STRENGTH = "strength", "Силовая"
        CARDIO = "cardio", "Кардио"
        STRETCHING = "stretching", "Растяжка"
        SWIMMING = "swimming", "Плавание"
        RUNNING = "running", "Бег"
        CYCLING = "cycling", "Велосипед"
        OTHER = "other", "Другое"

    date = models.DateField(verbose_name='Дата')
    title = models.CharField(
        max_length=20,
        choices=Title.choices,
        default=Title.STRENGTH,
        verbose_name='Вид тренировки'
    )
    duration_minutes = models.PositiveIntegerField(verbose_name='Длительность(мин)')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date'] #от свежих к старым

    def __str__(self):
        return f"{self.date}: {self.get_title_display()}"


class NutritionEntry(models.Model):
    date = models.DateField(unique=True, verbose_name='Дата')
    calories = models.PositiveIntegerField(verbose_name='Ккал')
    protein = models.PositiveIntegerField(null=True, blank=True, verbose_name='Б')
    fat = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ж')
    carbs = models.PositiveIntegerField(null=True, blank=True, verbose_name='У')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date'] #от свежих к старым
        verbose_name = "Nutrition entry"
        verbose_name_plural = "Nutrition entries" # чтобы не entrys

    def __str__(self):
        return f'{self.date}: {self.calories} kcal'


class Measurement(models.Model):
    date = models.DateField(unique=True, verbose_name="Дата")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Вес')
    waist = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='Талия')
    hips =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name="Бедра")
    chest =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name="Грудь")
    thigh =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name="Бедро")
    biceps =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name="Бицепс")
    calf =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name="Голень")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date}: {self.weight} kg'


class UserProfile(models.Model):
    class Goal(models.TextChoices):
        LOSE = 'lose', 'Похудение'
        MAINTAIN = 'maintain', 'Поддержание веса'
        GAIN = 'gain', 'Набор массы'

    class Gender(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'

    class Activity(models.TextChoices):
        SEDENTARY = 'sedentary', 'Сидячий образ жизни'
        LIGHT = 'light', 'Лёгкая активность (1-3 раза в неделю)'
        MODERATE = 'moderate', 'Средняя (3-5 раз в неделю)'
        ACTIVE = 'active', 'Высокая (6-7 раз в неделю)'
        VERY_ACTIVE = 'very_active', 'Очень высокая (физическая работа)'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activity = models.CharField(
        max_length=20,
        choices=Activity.choices,
        default=Activity.MODERATE,
        verbose_name='Активность'
    )
    goal = models.CharField(
        max_length=20,
        choices=Goal.choices,
        default=Goal.MAINTAIN,
        verbose_name='Цель'
    )
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        verbose_name='Пол'
    )
    age = models.PositiveIntegerField(verbose_name='Возраст', validators=[MinValueValidator(14), MaxValueValidator(100)])
    weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='Вес, кг',
        validators=[MinValueValidator(30), MaxValueValidator(300)],
    )
    height = models.PositiveIntegerField(verbose_name='Рост', validators=[MinValueValidator(100), MaxValueValidator(250)])

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.user.username} — {self.get_goal_display()}"
