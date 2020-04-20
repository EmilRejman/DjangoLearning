from django.urls import path, include
from . import views
from django.conf import settings
from . import views as register_views

app_name = 'register'  # with this the django knows which {% url %} use when there are a lot of applications in the project
urlpatterns = [
    path('', include('django.contrib.auth.urls')), #for login, logout, password management
    #registration as different app
    path('register/', register_views.register, name="register"),
]

