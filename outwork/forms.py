from django.forms import ModelForm
from django import forms
from .models import UserData, Workout


class RegisterForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['bio', 'dob', 'height_feet', 'height_inches', 'weight', 'spotify_playlist_uri']
        labels = {
            'dob': 'Date of birth',
            'height_feet': 'Height (ft)',
            'height_inches': 'Height (in)',
            'spotify_playlist_uri': 'Spotify URI of your favorite workout playlist',
        }
        help_texts = {
            'bio': 'A brief message about yourself',
            'dob': 'Use format (MM/DD/YYYY)',
            'spotify_playlist_uri': "To find your spotify playlist's URI, click on the '...' under the playlist "
                                    "description. Then click 'Share' while holding down ALT and then select "
                                    "'Copy Spotify URI'. Optional"
        }


class RunningForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'calories', 'length', 'distance', 'notes']
        labels = {
            'date': 'Date of Run (MM/DD/YYYY)',
            'calories': 'Total Calories Burned',
            'length': 'Duration of Run (in minutes)',
            'distance': 'Length of run (mi)',
        }
        help_texts = {
            'date': 'Use format (MM/DD/YYYY)',
        }

class LiftingForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'calories', 'length', 'sets', 'reps', 'weight', 'notes']
        labels = {
            'date': 'Date of Workout (MM/DD/YYYY)',
            'calories': 'Total Calories Burned',
            'length': 'Duration of Workout (in minutes)',
            'weight': 'Weight (lbs)',
        }
        help_texts = {
            'date': 'Use format (MM/DD/YYYY)',
        }


class OtherForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'calories', 'length', 'distance', 'sets', 'reps', 'weight', 'notes']
        labels = {
            'date': 'Date of Workout (MM/DD/YYYY)',
            'calories': 'Total Calories Burned',
            'length': 'Duration of Workout (in minutes)',
            'distance': 'Distance of Workout (in miles)',
            'weight': 'Weight (lbs)',
        }
        help_texts = {
            'date': 'Use format (MM/DD/YYYY)',
        }

