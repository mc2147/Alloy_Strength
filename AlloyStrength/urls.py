from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from Users.views import * 

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^admin-workouts/', Admin_Workouts, name='AdminWorkouts'),
    url(r'^admin-workouts-2/', Admin_Workouts_2, name='Home'),
    url(r'^admin-workouts-3/', Admin_Workouts_3, name='Home'),
    url(r'^admin-workouts-4/', Admin_Workouts_4, name='Home'),

    url(r'^admin-home/', Admin_Home, name="AdminHome"),
    url(r'^admin-exercises/', AdminExercises, name='AdminExercises'),
    url(r'^admin-videos/', Admin_Videos, name='AdminVideos'),
    url(r'^admin-videos-2/', Admin_Videos_2, name=''),    
    url(r'^admin-videos-library/', Admin_Videos_Library, name='Home'),
    url(r'^admin-videos-library-edit/', Admin_Videos_Edit, name='Home'),

    url(r'^admin-users/', Admin_Users, name='AdminUsers'),
    url(r'^admin-users-view-profile/', Admin_User_Profile, name='AdminUserProfile'),

    url(r'^home/', Home, name='Home'),
    url(r'^member-home/', Member_Home, name='Home'),
    url(r'^test/', Test, name='Test'),
    url(r'^stripe-test/', Stripe_Test, name='Stripe Test'),
    url(r'^userpage/', User_Page, name="userpage"),
    url(r'^userpageUpdate/', Workout_Update, name="userpageUpdate"),
    url(r'^userpageRPEUpdate/', RPE_Update, name="userpageRPEUpdate"),
    url(r'^videos/', Videos, name="userpage")
]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

