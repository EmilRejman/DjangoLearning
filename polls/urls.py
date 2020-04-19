from django.urls import path
from . import views
from django.conf import settings

# this urls are included with funcion 'include' to main catalog mysite\urls thats why app's urls are in main urls
app_name = 'polls'  # with this the django knows which {% url %} use when there are a lot of applications in the project
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # version with view
    path('<int:question_id>/vote/', views.vote, name='vote'),  # hard way of URL, withou usage of generic views
    path('add_question/', views.AddQuestion, name='AddQuestion')
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
