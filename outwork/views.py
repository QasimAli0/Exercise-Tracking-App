from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, request
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .forms import RegisterForm, RunningForm, LiftingForm, OtherForm
from .models import UserData, Workout, Follows
from django.shortcuts import render
from django.db import IntegrityError
import datetime
from django import forms
from django.views import generic
from django.utils import timezone
from django.views.generic.detail import DetailView

# Create your views here.


def index(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return render(request, 'outwork/index.html')


def register(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))
    if request.user.is_authenticated:
        if request.method == 'POST':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                new_userdata = register_form.save(commit=False)
                new_userdata.user = request.user
                new_userdata.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))
        else:
            register_form = RegisterForm()
        return render(request, 'outwork/register.html', {'register_form': register_form})


def profile(request, username=""):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        if username == "":
            username = request.user.username

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if UserData.objects.filter(user_id=user.id).exists():
                userdata = UserData.objects.get(user_id=user.id)
                # Calculate total calories for past week

                playlist_json = {}
                if userdata.spotify_playlist_uri != "":
                    playlist_json = userdata.get_playlist_information()
                    if 'error' in playlist_json:
                        playlist_json = {}

                is_current_user = False
                if request.user.username == username:
                    is_current_user = True

                if is_current_user and request.method == "POST":
                    following_userdata = userdata
                    follower_username = request.POST.get('username_input', None)
                    if User.objects.filter(username=follower_username).exists():
                        follower_user = User.objects.get(username=follower_username)
                        if UserData.objects.filter(user_id=follower_user.id).exists():
                            follower_userdata = UserData.objects.get(user_id=follower_user.id)

                            if follower_userdata == following_userdata:
                                return HttpResponse("You cannot follow yourself")
                            try:
                                Follows.objects.create(userdata=following_userdata, is_following=follower_userdata)
                            except IntegrityError:
                                return HttpResponse("You already follow this user")

                        else:
                            return HttpResponse("This person hasn't registered yet")

                    else:
                        return HttpResponse("This person doesn't exist")

                following = userdata.following.all()
                followers = userdata.followers.all()
                workouts = Workout.objects.filter(user=userdata).order_by('-date')[:10]
                level, xp = userdata.get_level_and_xp()
                progress = int(xp/10)
                return render(request, 'outwork/profile.html', {'userdata': userdata,
                                                                'is_current_user': is_current_user,
                                                                'level': level,
                                                                'xp': xp,
                                                                'progress': progress,
                                                                'workouts': workouts,
                                                                'following': following,
                                                                'followers': followers,
                                                                'playlist': playlist_json})

            else:
                return HttpResponse("This person hasn't registered yet")

        else:
            return HttpResponse("This person doesn't exist")

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def new_run(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        if request.method == 'POST':
            workout_form = RunningForm(request.POST)

            if workout_form.is_valid():
                workout_object = workout_form.save(commit=False)
                workout_object.user = UserData.objects.filter(user_id=request.user.id).first()
                workout_object.type = 'Running'
                if workout_object.calories == 0 or workout_object.calories is None:
                    workout_object.calories = workout_object.calories_running()
                workout_object.calculate_points()

                workout_object.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'username': workout_object.user.user.username}))

        else:
            workout_form = RunningForm()
        return render(request, 'outwork/new_workout.html', {'workout_form': workout_form})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def new_lift(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        if request.method == 'POST':
            workout_form = LiftingForm(request.POST)

            if workout_form.is_valid():
                workout_object = workout_form.save(commit=False)
                workout_object.user = UserData.objects.filter(user_id=request.user.id).first()
                workout_object.type = 'Weight Lifting'
                workout_object.total_weight_lifted = workout_object.reps * workout_object.sets * workout_object.weight
                workout_object.calculate_points()
                workout_object.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'username': workout_object.user.user.username}))

        else:
            workout_form = LiftingForm()
        return render(request, 'outwork/new_workout.html', {'workout_form': workout_form})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def new_other(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        if request.method == 'POST':
            workout_form = OtherForm(request.POST)

            if workout_form.is_valid():
                workout_object = workout_form.save(commit=False)
                workout_object.user = UserData.objects.filter(user_id=request.user.id).first()
                workout_object.type = 'Other'
                workout_object.total_weight_lifted = workout_object.reps * workout_object.sets * workout_object.weight
                workout_object.calculate_points()
                workout_object.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'username': workout_object.user.user.username}))

        else:
            workout_form = OtherForm()
        return render(request, 'outwork/new_workout.html', {'workout_form': workout_form})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def follow_user(request, username=""):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if UserData.objects.filter(user_id=user.id).exists():
                following_userdata = UserData.objects.filter(user_id=request.user.id).first()
                follower_userdata = UserData.objects.get(user_id=user.id)

                if follower_userdata == following_userdata:
                    return HttpResponse("You cannot follow yourself")
                try:
                    Follows.objects.create(userdata=following_userdata, is_following=follower_userdata)
                except IntegrityError:
                    return HttpResponse("You already follow this user")

                return HttpResponseRedirect(reverse('user_list'))

            else:
                return HttpResponse("This person hasn't registered yet")
        else:
            return HttpResponse("This person doesn't exist")

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def user_list(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

            users_list = UserData.objects.all()
            following = UserData.objects.get(user_id=request.user.id).following.all()
            users = []
            for user in users_list:
                if request.user.username == user.user.username:
                    continue
                else:
                    users.append(user)
                    for follow in following:
                        if follow.is_following.user.username == user.user.username:
                            users.pop()
                            break
            return render(request, 'outwork/user_list.html', {'users': users})
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def leadership_board(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        # -----------Turn into function that returns sorted list of users----------
        users_list = UserData.objects.all()
        leaderboard = []
        for user in users_list:
            calories = user.total_cals()
            leaderboard.append((user, calories))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        # -------------------------------------------------------------------------

        return render(request, 'outwork/leadership_board.html', {'leaderboard': leaderboard})
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))

    
def leadership_board_cals(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():
        userdata = UserData.objects.get(user_id=request.user.id)
        users_list = userdata.following.all()
        leaderboard = []
        calories = userdata.total_cals()
        leaderboard.append((userdata, calories))
        for user in users_list:
            calories = user.is_following.total_cals()
            leaderboard.append((user.is_following, calories))

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        for i in range(len(leaderboard)):
            leaderboard[i][0].rank = i + 1

        return render(request, 'outwork/calories_leadership.html', {'leaderboard': leaderboard})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def leadership_board_distance(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        userdata = UserData.objects.get(user_id=request.user.id)
        users_list = userdata.following.all()
        leaderboard = []
        distance = userdata.total_distance()
        leaderboard.append((userdata, distance))
        for user in users_list:
            distance = user.is_following.total_distance()
            leaderboard.append((user.is_following, distance))

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        for i in range(len(leaderboard)):
            leaderboard[i][0].rank = i + 1

        return render(request, 'outwork/distance_leadership.html', {'leaderboard': leaderboard})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def leadership_board_weight(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        userdata = UserData.objects.get(user_id=request.user.id)
        users_list = userdata.following.all()
        leaderboard = []
        weight = userdata.total_weight()
        leaderboard.append((userdata, weight))
        for user in users_list:
            weight = user.is_following.total_weight()
            leaderboard.append((user.is_following, weight))

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        for i in range(len(leaderboard)):
            leaderboard[i][0].rank = i + 1

        return render(request, 'outwork/weight_leadership.html', {'leaderboard': leaderboard})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))

    
def edit_profile(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        userdata = UserData.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                changed_userdata = form.save(commit=False)

                if changed_userdata.bio != "":
                    userdata.bio = changed_userdata.bio

                if changed_userdata.dob is not None:
                    userdata.dob = changed_userdata.dob

                if changed_userdata.height_feet is not None:
                    userdata.height_feet = changed_userdata.height_feet

                if changed_userdata.height_inches is not None:
                    userdata.height_inches = changed_userdata.height_inches

                if changed_userdata.weight is not None:
                    userdata.weight = changed_userdata.weight

                if changed_userdata.spotify_playlist_uri != "":
                    userdata.spotify_playlist_uri = changed_userdata.spotify_playlist_uri

                userdata.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))

        else:
            form = RegisterForm(initial={
                'bio': userdata.bio,
                'dob': userdata.dob,
                'height_feet': userdata.height_feet,
                'height_inches': userdata.height_inches,
                'weight': userdata.weight,
                'spotify_playlist_uri': userdata.spotify_playlist_uri,

            })
        return render(request, 'outwork/edit_profile.html', {'form': form})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def remove_follower(request, username=""):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if UserData.objects.filter(user_id=user.id).exists():
                to_be_deleted = UserData.objects.get(user_id=user.id)

                current_user = UserData.objects.filter(user_id=request.user.id).first()
                if Follows.objects.filter(userdata=current_user, is_following=to_be_deleted).exists():
                    Follows.objects.filter(userdata=current_user, is_following=to_be_deleted).delete()
        return HttpResponseRedirect(reverse('edit_workouts_and_followers'))
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def remove_workout(request, workout_id):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        if Workout.objects.filter(id=workout_id).exists():
            workout = Workout.objects.get(id=workout_id)
            userdata = UserData.objects.get(user_id=request.user.id)
            if workout.user == userdata:
                workout.delete()
        return HttpResponseRedirect(reverse('edit_workouts_and_followers'))
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))


def edit_workouts_and_followers(request):
    if request.user.is_authenticated and UserData.objects.filter(user_id=request.user.id).exists():

        userdata = UserData.objects.filter(user_id=request.user.id).first()

        following = userdata.following.all()
        workouts = Workout.objects.filter(user=userdata).order_by('-date')
        return render(request, 'outwork/remove_follow_and_workout.html', {'userdata': userdata,
                                                                'workouts': workouts,
                                                                'following': following,})

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return HttpResponseRedirect(reverse('index'))
