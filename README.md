# A-06 [Outwork](https://out-work.herokuapp.com)

Outwork is a web application built using the django framework designed to gamify exercise.
Users can track their workouts, earn points and level up, and connect with their friends.


### Logging in and Registering:

When a user first opens the site, they are prompted to sign in with their google account.
After clicking "Login with Google" the user will be redirected to google sign in. Once signed
in, the user will be redirected to the register page, where they can fill in some information
about themselves. All of the fields are optional. If you do not have a spotify account, an
example Spotify URI is: 'spotify:playlist:37i9dQZEVXbLRQDuF5jeBp'. This is the URI of Spotify's
"Top 50 - USA" playlist. Once the form for registering has been submitted, the user is 
redirected to their profile page.

### The Profile Page:

Each user's profile page displays their 10 most recent workouts as well as their followers and
the people they are following. If the user decided to share their workout playlist, a link
to their playlist will also be displayed.

### Connecting with Other Users:
If a user would like to find other users to follow, they can click on the "Find Users"
button in the navigation bar at the top of the screen. This page displays a list of all 
users that are not followed by the current user. THe "Follow User" button next to each
name can be clicked to follow that user. The user's profile page also has a space in the
"Who You are Following" card where users can be followed by username.


### Tracking Workouts:
Once a user has registered and connected with their friends, they can start tracking their
workouts!. The "Add Workout" button on the navigation bar can be clicked to display the 
different workouts available to add. Clicking on a workout type will redirect the user to
a form to input the details of their workout. Once the form is submitted, the user is redirected
to their profile page where they will see the new workout and the number of points gained from it.

### Editing Profile, Workouts, and Followers
Under the account tab in the navigation bar, users can use the "Edit Profile" and
"Edit Workout/Followers" buttons to make changes to their account. The edit profile page
allows users to change the information they gave when initially registering. The edit 
workouts and followers page allows users to delete their past workouts and unfollow users.

### Sources Used:
Title: Django\
Author: https://github.com/django/djangoproject.com/graphs/contributors  
Date: 05/4/2021\
Code version: 3.1.5\
URL: https://www.djangoproject.com/\
Software License: BSD-3-Clause License

Title: Django Heroku\
Author: Kenneth Reitz\
Date: 02/14/2021\
Code version: 0.3.1\
URL: https://pypi.org/project/django-heroku/  
Software License: MIT License

Title: Bootstrap\
Author: Mark Otto, Jacob Thornton\
Date: 02/14/2021\
Code version: 4.0\
URL: https://github.com/twbs/bootstrap  
Software License: MIT License

Title: Spotify Web API\
Author: Spotify\
Date: 02/14/2021\
URL: https://developer.spotify.com/documentation/web-api/  
Software License: https://developer.spotify.com/terms/#iii  

Title: PostgreSQL\
Author: Michael Stonebraker\
Date: 02/14/2021\
URL: https://github.com/postgres/postgres  
Software License: PostgreSQL License
