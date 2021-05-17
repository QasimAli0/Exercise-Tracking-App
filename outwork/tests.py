from django.test import TestCase, RequestFactory
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserData, Workout, Follows
from .views import profile, new_run, new_lift, new_other, follow_user, register, \
    leadership_board_cals, leadership_board_weight, leadership_board_distance, user_list
from django.urls import reverse
# Create your tests here.


class WorkoutModelTests(TestCase):

    def test_is_recent_with_very_old_workout(self):
        q = Workout(date=datetime.date(2020, 4, 20))
        self.assertEqual(q.is_recent(), False)

    def test_is_recent_with_old_workout(self):
        q = Workout(date=datetime.date.today() - datetime.timedelta(days=7))
        self.assertEqual(q.is_recent(), False)

    def test_is_recent_with_recent_workout(self):
        q = Workout(date=datetime.date.today() - datetime.timedelta(days=4))
        self.assertEqual(q.is_recent(), True)

    def test_is_recent_with_new_workout(self):
        q = Workout(date=datetime.date.today())
        self.assertEqual(q.is_recent(), True)

    def test_is_recent_with_future_workout(self):
        q = Workout(date=datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(q.is_recent(), False)


class RegisterViewTests(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create(username='Tester', id=1, first_name="firstname", last_name="lastname")

    def test_user_cannot_register_twice(self):
        request = self.rf.get('/')
        request.user = self.user
        userdata = UserData(user=self.user, bio="Hello I am the Tester", id=1)
        userdata.save()
        response = register(request)
        self.assertEqual(response.status_code, 302)

    def test_user_is_unregistered(self):
        request = self.rf.get('/')
        request.user = self.user
        response = register(request)
        self.assertEqual(response.status_code, 200)


class ProfileViewTests(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create(username='Tester', id=1, first_name="firstname", last_name="lastname")
        self.userdata = UserData(user=self.user, bio="Hello I am the Tester", id=1)
        self.userdata.save()

    def test_user_does_not_exist(self):
        """
        If a user does not exist, an appropriate message is displayed.
        EX: /profile/Tester
        """
        request = self.rf.get('/')
        request.user = self.user
        response = profile(request, username="fakeUsername")
        self.assertContains(response, "This person doesn't exist")

    def test_user_exists_but_profile_is_not_registered(self):
        """
        If a user exists but has not registered their
        profile (by entering their user data), they are redirected to the register page.
        """
        request = self.rf.get('/')
        request.user = User.objects.create(username='Tester2', id=2, first_name="firstname", last_name="lastname")
        response = profile(request, username=request.user.username)
        self.assertEqual(response.status_code, 302)  # got redirected somewhere else

    def test_user_exists_and_profile_is_registered(self):
        """
        If an existing user has registered, their bio and workout data are displayed.
        EX: /profile/jacob
        """
        request = self.rf.get('/')
        request.user = self.user
        url = reverse('profile', args=("test",))
        response = profile(request, username=request.user.username)
        self.assertEqual(response.status_code, 200)


class NewWorkoutViewTests(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create(username='Tester', id=1, first_name="firstname", last_name="lastname")
        self.userdata = UserData(user=self.user, bio="Hello I am the Tester", id=1)
        self.userdata.save()

    def test_new_workout_running(self):
        """
        If the user attempts to add a running workout, the proper form is presented.
        EX: /new_workout/running
        """
        request = self.rf.get('/')
        request.user = self.user
        response = new_run(request)
        self.assertEqual(response.status_code, 200)

    def test_new_workout_lifting(self):
        """
        If the user attempts to add a lifting workout, the proper form is presented.
        EX: /new_workout/lifting
        """
        request = self.rf.get('/')
        request.user = self.user
        response = new_lift(request)
        self.assertEqual(response.status_code, 200)

    def test_new_workout_other(self):
        """
        If the user attempts to add an other workout, the proper form is presented.
        EX: /new_workout/other
        """
        request = self.rf.get('/')
        request.user = self.user
        response = new_other(request)
        self.assertEqual(response.status_code, 200)


class UserListViewTests(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create(username='Tester', id=1, first_name="firstname", last_name="lastname")
        self.userdata = UserData(user=self.user, bio="Hello I am the Tester", id=1)
        self.userdata.save()

    def test_logged_in_and_registered_user(self):
        """
        If a user tries to follow a user that does not exist, an appropriate message is displayed.
        """
        request = self.rf.get('/')
        request.user = self.user
        response = user_list(request)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_but_not_registered_user(self):
        """
        If a user tries to follow a user that does not exist, an appropriate message is displayed.
        """
        request = self.rf.get('/')
        request.user = self.user
        self.userdata.delete()
        response = user_list(request)
        self.assertEqual(response.status_code, 302)

    def test_correct_users_are_shown(self):
        """
        If a user tries to follow a user that exists but has not registered their profile yet, an appropriate message is displayed.
        """
        user = User.objects.create(username='unfollowed_user', id=2, first_name="firstname", last_name="lastname")
        data = UserData(user=user, bio="Hello I am the Tester's friend", id=2)
        user.save()
        data.save()
        request = self.rf.get('/')
        request.user = self.user
        response = user_list(request)
        self.assertContains(response, "unfollowed_user")

    def test_cannot_see_self(self):
        """
        If a user tries to follow themself, an appropriate message is displayed.
        """
        request = self.rf.post('/follow_user/', {'username_input': self.user.username})
        request.user = self.user
        response = follow_user(request)
        self.assertNotContains(response, "Tester")


class LeadershipBoardViewTests(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create(username='Tester', id=1, first_name="firstname", last_name="lastname")
        self.userdata = UserData(user=self.user, bio="Hello I am the Tester", id=1)
        self.userdata.save()

        # create second user
        other_user = User.objects.create(username='other', id=2, first_name="Other", last_name="Person")
        other_user.save()
        other_userdata = UserData(user=other_user, bio="Hello I am other person", id=2)
        other_userdata.save()

    def test_load_leadership_board_cals(self):
        """
        If a user accesses the leadership board, a ranking of users' workout data is displayed.
        """
        request = self.rf.get('/')
        request.user = self.user
        response = leadership_board_cals(request)
        self.assertEqual(response.status_code, 200)

    def test_leadership_board_cals_displays_correct_numbers(self):
        # Create Workout for main user
        workout = Workout.objects.create(user=self.userdata, id=1, calories=100)
        workout.save()

        request = self.rf.get('/')
        request.user = self.user
        response = leadership_board_cals(request)
        self.assertContains(response, "100 Calories Burned")

    def test_load_leadership_board_weight(self):
        """
        If a user accesses the leadership board, a ranking of users' workout data is displayed.
        """
        request = self.rf.get('/')
        request.user = self.user
        response = leadership_board_weight(request)
        self.assertEqual(response.status_code, 200)

    def test_leadership_board_weight_displays_correct_numbers(self):
        # Create Workout for main user
        workout = Workout.objects.create(user=self.userdata, id=1, calories=100)
        workout.total_weight_lifted = 777
        workout.type = 'Weight Lifting'
        workout.save()

        request = self.rf.get('/')
        request.user = self.user
        response = leadership_board_weight(request)
        self.assertContains(response, "Total weight lifted: 777 lbs")

    def test_load_leadership_board_distance(self):
        """
        If a user accesses the leadership board, a ranking of users' workout data is displayed.
        """
        request = self.rf.get('/')
        request.user = self.user
        response = leadership_board_distance(request)
        self.assertEqual(response.status_code, 200)

    def test_leadership_board_distance_displays_correct_numbers(self):
        # Create Workout for main user
        workout = Workout.objects.create(user=self.userdata, id=1, calories=100)
        workout.distance = 4
        workout.type = 'Running'
        workout.save()

        request = self.rf.get('/')
        request.user = self.user
        response = leadership_board_distance(request)
        self.assertContains(response, "Total distance: 4 miles")


class SpotifyAPITests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Tester', id=1, first_name="firstname", last_name="lastname")
        self.userdata = UserData(user=self.user, bio="Hello I am the Tester", id=1)
        self.userdata.save()

    def test_bad_uri(self):
        self.userdata.spotify_playlist_uri = 'bad'
        self.userdata.save()
        json = self.userdata.get_playlist_information()
        self.assertEqual(json, {})

    def test_top_50_USA_uri(self):
        self.userdata.spotify_playlist_uri = 'spotify:playlist:37i9dQZEVXbLRQDuF5jeBp'
        self.userdata.save()
        json = self.userdata.get_playlist_information()
        self.assertEqual(json['name'], 'Top 50 - USA')

    def test_modern_rock(self):
        self.userdata.spotify_playlist_uri = 'spotify:playlist:37i9dQZF1DX1helbHcrYM1'
        self.userdata.save()
        json = self.userdata.get_playlist_information()
        self.assertEqual(json['name'], 'Modern Rock')
