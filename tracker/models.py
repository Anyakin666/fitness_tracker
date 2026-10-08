from django.db import models

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

    date = models.DateField()
    title = models.CharField(
        max_length=20,
        choices=Title.choices,
        default=Title.STRENGTH,
    )
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date'] #от свежих к старым

    def __str__(self):
        return f"{self.date}: {self.get_title_display()}"


class NutritionEntry(models.Model):
    date = models.DateField(unique=True)
    calories = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    fat = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()

    class Meta:
        ordering = ['-date'] #от свежих к старым

    def __str__(self):
        return f'{self.date}: {self.calories} kcal'


class Measurement(models.Model):
    date = models.DateField(unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    waist = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    hips =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    chest =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    thigh =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    biceps =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    calf =  models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date}: {self.weight}'