from django.conf.urls import url
from django.contrib import admin
from Users.views import Home, Member_Home, Admin, Test, User_Page, Workout_Update, Videos, AdminExercises, RPE_Update

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin-site/', Admin, name='Home'),
    url(r'^admin-exercises/', AdminExercises, name='Home'),
    url(r'^home/', Home, name='Home'),
    url(r'^member-home/', Member_Home, name='Home'),
    url(r'^test/', Test, name='Test'),
    url(r'^userpage/', User_Page, name="userpage"),
    url(r'^userpageUpdate/', Workout_Update, name="userpageUpdate"),
    url(r'^userpageRPEUpdate/', RPE_Update, name="userpageRPEUpdate"),
    url(r'^videos/', Videos, name="userpage")
]
