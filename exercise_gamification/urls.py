"""exercise_gamification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from outwork import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('follow_user/<str:username>/', views.follow_user, name='follow_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('remove_follow/<str:username>', views.remove_follower, name='remove_follow'),
    path('remove_workout/<int:workout_id>', views.remove_workout, name='remove_workout'),
    path('edit_workouts_and_followers/', views.edit_workouts_and_followers, name='edit_workouts_and_followers'),

    # path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/cals', views.leadership_board_cals, name='leadership_board_cals'),
    path('leaderboard/distance', views.leadership_board_distance, name='leadership_board_distance'),
    path('leaderboard/weight', views.leadership_board_weight, name='leadership_board_weight'),

    path('new_workout/running/', views.new_run, name='running'),
    path('new_workout/lifting/', views.new_lift, name='lifting'),
    path('new_workout/other/', views.new_other, name='other'),

    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),

]
