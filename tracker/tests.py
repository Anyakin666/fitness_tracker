from django.test import TestCase
from django.contrib.auth.models import User
from .models import Workout, NutritionEntry, Measurement
from django.urls import reverse
from decimal import Decimal
from datetime import date


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


class WorkoutCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')

    def test_requires_login(self):
        response = self.client.get(reverse('workout_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_create_workout(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('workout_add'), {
            'date': '2026-10-20',
            'title': 'strength',
            'duration_minutes': 60,
            'notes': 'kokopuhi',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Workout.objects.count(), 1)
        workout = Workout.objects.first()
        self.assertEqual(workout.user, self.user)
        self.assertEqual(workout.title, 'strength')
        self.assertEqual(workout.notes, 'kokopuhi')


class NutritionCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test2', password='test123')

    def test_requires_login(self):
        response = self.client.get(reverse('nutrition_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_create_nutrition(self):
        self.client.login(username='test2', password='test123')
        response = self.client.post(reverse('nutrition_add'), {
            'date': '2026-10-20',
            'calories': 1950,
            'protein': 120,
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(NutritionEntry.objects.count(), 1)
        nutrition = NutritionEntry.objects.first()
        self.assertEqual(nutrition.user, self.user)
        self.assertEqual(nutrition.calories, 1950)
        self.assertEqual(nutrition.protein, 120)


class MeasurementCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test3', password='test123')

    def test_requires_login(self):
        response = self.client.get(reverse('measurement_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_create_measurement(self):
        self.client.login(username='test3', password='test123')
        response = self.client.post(reverse('measurement_add'), {
            'date' : '2026-10-20',
            'weight' : '61.15',
            'waist': '74.1',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Measurement.objects.count(), 1)
        measurement = Measurement.objects.first()
        self.assertEqual(measurement.user, self.user)
        self.assertEqual(measurement.weight, Decimal('61.15'))
        self.assertEqual(measurement.waist, Decimal('74.1'))


class WorkoutDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.workout = Workout.objects.create(
            user=self.user, date='2026-10-20', title='strength', duration_minutes=60,
        )

    def test_requires_login(self):
        response = self.client.get(reverse('workout_delete', args=[self.workout.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_delete_workout(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('workout_delete', args=[self.workout.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Workout.objects.count(), 0)


class NutritionDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.nutrition = NutritionEntry.objects.create(
            user=self.user, date='2026-10-20', calories=1800,
        )

    def test_requires_login(self):
        response = self.client.get(reverse('nutrition_delete', args=[self.nutrition.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_delete_nutrition(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('nutrition_delete', args=[self.nutrition.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NutritionEntry.objects.count(), 0)


class MeasurementDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.measurement = Measurement.objects.create(
            user=self.user, date='2026-10-20', weight=60, waist=50,
        )

    def test_requires_login(self):
        response = self.client.get(reverse('measurement_delete', args=[self.measurement.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_delete_measurement(self):
        self.client.login(username='test', password='test123')
        response = self.client.post(reverse('measurement_delete', args=[self.measurement.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Measurement.objects.count(), 0)


class WorkoutUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='editor', password='test123')
        self.workout = Workout.objects.create(
            user=self.user, date='2026-10-20', title='strength',
            duration_minutes=60, notes='old notes',
        )

    def test_requires_login(self):
        response = self.client.get(reverse('workout_edit', args=[self.workout.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_update_workout(self):
        self.client.login(username='editor', password='test123')
        response = self.client.post(reverse('workout_edit', args=[self.workout.pk]), {
            'date': '2026-10-21',
            'title': 'cardio',
            'duration_minutes': 45,
            'notes': 'new notes',
        })
        self.assertEqual(response.status_code, 302)

        self.workout.refresh_from_db()  
        self.assertEqual(self.workout.title, 'cardio')
        self.assertEqual(self.workout.duration_minutes, 45)
        self.assertEqual(self.workout.notes, 'new notes')
        self.assertEqual(self.workout.date, date(2026, 10, 21))


class NutritionUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='editor', password='test123')
        self.nutrition = NutritionEntry.objects.create(
            user=self.user, date='2026-10-20', calories=1800,
            protein=120, fat=50, carbs=200,
        )

    def test_requires_login(self):
        response = self.client.get(reverse('nutrition_edit', args=[self.nutrition.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_update_nutrition(self):
        self.client.login(username='editor', password='test123')
        response = self.client.post(reverse('nutrition_edit', args=[self.nutrition.pk]), {
            'date': '2026-10-21',
            'calories': 2100,
            'protein': 130,
            'fat': 61,
            'carbs' : 210,
        })
        self.assertEqual(response.status_code, 302)

        self.nutrition.refresh_from_db()  
        self.assertEqual(self.nutrition.calories, 2100)
        self.assertEqual(self.nutrition.protein, 130)
        self.assertEqual(self.nutrition.fat, 61)
        self.assertEqual(self.nutrition.carbs, 210)
        self.assertEqual(self.nutrition.date, date(2026, 10, 21))


class MeasurementUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='editor', password='test123')
        self.measurement = Measurement.objects.create(
            user=self.user, date='2026-10-20', weight=60.00, waist=74.1
        )

    def test_requires_login(self):
        response = self.client.get(reverse('measurement_edit', args=[self.measurement.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_update_measurement(self):
        self.client.login(username='editor', password='test123')
        response = self.client.post(reverse('measurement_edit', args=[self.measurement.pk]), {
            'date': '2026-10-21',
            'weight' : '70.00',
            'waist' : '75.1',
        })
        self.assertEqual(response.status_code, 302)

        self.measurement.refresh_from_db()  
        self.assertEqual(self.measurement.weight, Decimal('70.00'))
        self.assertEqual(self.measurement.waist, Decimal('75.1'))
        self.assertEqual(self.measurement.date, date(2026, 10, 21))
        