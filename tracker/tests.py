from django.test import TestCase
from django.contrib.auth.models import User
from .models import Workout, NutritionEntry, Measurement


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')

    def test_create_workout(self):
        workout = Workout.objects.create(
            user=self.user,
            date='2026-10-20',
            title='strength',
            duration_minutes=60,
        )
        self.assertEqual(workout.title, 'strength')
        self.assertEqual(workout.user, self.user)
        self.assertEqual(Workout.objects.count(), 1)

    def test_str(self):
        workout = Workout.objects.create(
            user=self.user,
            date='2026-10-16',
            title='cardio',
            duration_minutes=20,
        )
        self.assertEqual(str(workout), "2026-10-16: Кардио")

    def test_get_title_display(self):
        workout = Workout.objects.create(
            user=self.user,
            date='2026-10-17',
            title='running',
            duration_minutes=30,
        )
        self.assertEqual(workout.get_title_display(), 'Бег')


class NutritionEntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test2', password='test123')

    def test_create_nutrition_entry(self):
        entry = NutritionEntry.objects.create(
            user=self.user,
            date='2026-10-20',
            calories=2000,
            protein=100,
            fat=60,
            carbs=250,
        )
        self.assertEqual(entry.calories, 2000)
        self.assertEqual(entry.user, self.user)
        self.assertEqual(NutritionEntry.objects.count(), 1)

    def test_str(self):
        entry = NutritionEntry.objects.create(
            user=self.user,
            date='2026-10-20',
            calories=2000,
        )
        self.assertEqual(str(entry), "2026-10-20: 2000 kcal")


class MeasurementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test3', password='test123')

    def test_create_measurement(self):
        measurement = Measurement.objects.create(
            user=self.user,
            date='2026-10-20',
            weight=60,
            waist=70,
        )
        self.assertEqual(measurement.weight, 60)
        self.assertEqual(measurement.waist, 70)
        self.assertEqual(measurement.user, self.user)
        self.assertEqual(Measurement.objects.count(), 1)

    def test_str(self):
        measurement = Measurement.objects.create(
            user=self.user,
            date='2026-10-16',
            weight=65,
        )
        self.assertEqual(str(measurement), '2026-10-16: 65 kg')

# Create your tests here.
