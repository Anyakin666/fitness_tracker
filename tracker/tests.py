from django.test import TestCase
from django.contrib.auth.models import User
from .models import Workout, NutritionEntry, Measurement
from django.urls import reverse


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


class WorkoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='test123')
        self.other = User.objects.create_user(username='other', password='test123')

        self.my_workout = Workout.objects.create(
            user=self.user, date='2026-10-20', title='strength', duration_minutes=60,
        )
        self.other_workout = Workout.objects.create(
            user=self.other, date='2026-10-19', title='cardio', duration_minutes=30,
        )

    def test_requires_login(self):
        response = self.client.get(reverse('workout_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_shows_only_own_workouts(self):
        self.client.login(username='viewer', password='test123')
        response = self.client.get(reverse('workout_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.my_workout.get_title_display())
        self.assertNotContains(response, self.other_workout.get_title_display())


class NutritionViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='test123')
        self.other = User.objects.create_user(username='other', password='test123')
        
        self.my_nutrition = NutritionEntry.objects.create(
            user=self.user, date='2026-10-20', calories=1800)
        self.other_nutrition = NutritionEntry.objects.create(
            user=self.other, date='2026-10-19', calories=1600)

    def test_requires_login(self):
            response = self.client.get(reverse('nutrition_list'))
            self.assertEqual(response.status_code, 302)
            self.assertIn('/accounts/login/', response.url)

    def test_shows_only_own_nutritions(self):
            self.client.login(username='viewer', password='test123')
            response = self.client.get(reverse('nutrition_list'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.my_nutrition.calories)
            self.assertNotContains(response, self.other_nutrition.calories)


class MeasurementViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='test123')
        self.other = User.objects.create_user(username='other', password='test123')
        
        self.my_measurement = Measurement.objects.create(
            user=self.user, date='2026-10-20', weight=60.00, waist=70)
        self.other_measurement = Measurement.objects.create(
            user=self.other, date='2026-10-19', weight=50.00, waist=90)

    def test_requires_login(self):
            response = self.client.get(reverse('measurement_list'))
            self.assertEqual(response.status_code, 302)
            self.assertIn('/accounts/login/', response.url)

    def test_shows_only_own_measurements(self):
            self.client.login(username='viewer', password='test123')
            response = self.client.get(reverse('measurement_list'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.my_measurement.weight)
            self.assertNotContains(response, self.other_measurement.weight)        
# Create your tests here.
