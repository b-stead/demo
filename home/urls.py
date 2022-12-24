from django.urls import path
from . import views
from .views import HomeView, AboutView, ContactView
from .views import signup, signin, update_profile
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),

    path("password_reset/", views.password_reset_request, name="password_reset"),

    path("signup/", signup, name="signup"),
    #path("signin/", signin, name="signin"),
    path("update_profile/", update_profile, name="update_profile"),

]