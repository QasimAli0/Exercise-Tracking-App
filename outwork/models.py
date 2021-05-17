from json import JSONDecodeError

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from .utils import get_spotify_access_token
import requests


# Create your models here.


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    dob = models.DateField(null=True, blank=True, validators=[MaxValueValidator(datetime.date.today)])
    bio = models.TextField(null=True, blank=True, max_length=2000)
    height_feet = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    height_inches = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(11)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    spotify_playlist_uri = models.CharField(max_length=50, blank=True, default="")
    rank = models.PositiveSmallIntegerField(null=True)

    def add_friend(self, userid):
        userdata = UserData.objects.filter(user_id=userid).first()
        self.friends.add(userdata)
        self.save()

    def __str__(self):
        return self.user.username

    def get_playlist_information(self):
        access_token = get_spotify_access_token()
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        # Track ID from the URI
        if self.spotify_playlist_uri == "":
            return {}
        playlist_id = str(self.spotify_playlist_uri)[17:]

        # actual GET request with proper header
        try:
            return requests.get('https://api.spotify.com/v1/playlists/' + playlist_id, headers=headers).json()
        except JSONDecodeError:
            return {}

    def total_cals(self):
        workouts = Workout.objects.filter(user=self)
        total = 0
        for workout in workouts:
            total += workout.calories
        return total

    def total_distance(self):
        workouts = Workout.objects.filter(user=self)
        total = 0
        for workout in workouts:
            if workout.type == 'Running' or workout.type == 'Other':
                total += workout.distance
        return total

    def total_weight(self):
        workouts = Workout.objects.filter(user=self)
        total = 0
        for workout in workouts:
            if workout.type == 'Weight Lifting' or workout.type == 'Other':
                total += workout.total_weight_lifted
        return total

    def get_level_and_xp(self):
        workouts = Workout.objects.filter(user=self)
        points = 0
        for workout in workouts:
            points += workout.points

        level = points//1000
        xp = points % 1000
        return level, xp

    def get_recent_workouts(self):
        return Workout.objects.filter(user=self, date__gt=(datetime.date.today() - datetime.timedelta(days=7))).order_by('-date')


class Workout(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    date = models.DateField(null=True, validators=[MaxValueValidator(datetime.date.today)])

    TYPE_CHOICES = [
        ('Running', 'Running'),
        ('Weight Lifting', 'Weight Lifting'),
        ('Other', 'Other'),
    ]
    type = models.CharField(default='Running', choices=TYPE_CHOICES, max_length=50)
    calories = models.PositiveSmallIntegerField(null=True, validators=[MaxValueValidator(10000)])
    length = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(1440)])
    total_weight_lifted = models.PositiveIntegerField(null=True, default=0)
    distance = models.PositiveSmallIntegerField(null=True, validators=[MaxValueValidator(100)])
    reps = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(100)])
    sets = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(100)])
    weight = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(1000)])
    notes = models.TextField(null=True, blank=True, max_length=1000)
    points = models.PositiveIntegerField(default=0)

    def calculate_points(self):
        self.points += self.calories//2
        if self.type == 'Running' or self.type == 'Other':
            self.points += self.length * self.distance
        elif self.type == 'Weight Lifting' or self.type == 'Other':
            self.points += self.total_weight_lifted // 5
        else:
            self.points += 200

    def calories_running(self):
        if self.distance == 0 or self.length == 0:
            return 0
        met = 10
        avg_weight = 68
        # caloriesBurned = (avg_weight * met) * (self.length/60)
        # return caloriesBurned
        calories = (avg_weight * met) * (self.length/60)
        return calories

    def is_recent(self):
        now = timezone.now()
        return datetime.date.today() - datetime.timedelta(days=7) < self.date <= datetime.date.today()


class Follows(models.Model):
    userdata = models.ForeignKey(UserData, related_name='following', on_delete=models.CASCADE)
    is_following = models.ForeignKey(UserData, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userdata', 'is_following'],  name="unique_followers")
        ]
