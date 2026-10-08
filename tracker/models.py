from django.db import models

# Create your models here.
class Workout(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.date} - {self.title}'
