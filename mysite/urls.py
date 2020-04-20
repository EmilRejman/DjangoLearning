"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin, auth
from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView
from register import views as register_views
from django.views.generic import RedirectView


urlpatterns = [
    path('polls/', include('polls.urls')), # include() function allows referencing other URLconfs.
    path('admin/', admin.site.urls),

    # path('accounts/', include('django_registration.backends.one_step.urls')), # for registration
    # django_registration_register is the account-registration view.
    # django_registration_complete is the post-registration success message.
    # django_registration_activate is the account-activation view.
    # django_registration_activation_complete is the post-activation success message.
    # django_registration_disallowed is a message indicating registration is not currently permitted.
    # path('accounts/register/',
    #     RegistrationView.as_view(success_url='/polls/'), #default is "/profile/" #set the sucessful forwarding
    #     name='django_registration_register'),
    path('', include('django.contrib.auth.urls')), #for login, logout, password management
    #registration as different app
    path('register/', register_views.register, name="register"),
    path('', RedirectView.as_view(url='polls/', permanent=True)),
]
