from django.conf.urls import url
from django.contrib import admin
from Users.views import Home, Member_Home, Admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin-site/', Admin, name='Home'),
    url(r'^home/', Home, name='Home'),
    url(r'^member-home/', Member_Home, name='Home'),

]
