from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'team'
urlpatterns = [
    path('', views.TeamListView.as_view(), name='all_teams'),

    path('team/<int:pk>', views.TeamDetailView.as_view(), name='team_detail'),

    path('team/create',
        views.TeamCreateView.as_view(success_url=reverse_lazy('team:all_teams')), name='team_create'),
    path('<int:pk>/update',
        views.TeamUpdateView.as_view(success_url=reverse_lazy('team:all_teams')), name='team_update'),

    path('coaches/', views.CoachListView.as_view(), name='all_coaches'),
    path('coach/<int:pk>', views.CoachDetailView.as_view(), name='coach_detail'),

    path('coach/create',
        views.CoachCreateView.as_view(success_url=reverse_lazy('team:all_coaches')), name='coach_create'),
    path('coach/<int:pk>/update/',
        views.CoachUpdateView.as_view(success_url=reverse_lazy('team:all_coaches')), name='coach_update'),

    path('athletes/', views.AthleteListView.as_view(), name='all_athletes'),
    path('athlete/<int:pk>', views.AthleteDetailView.as_view(), name='athlete_detail'),

    path('athlete/create',
        views.AthleteCreateView.as_view(success_url=reverse_lazy('team:all_athletes')), name='athlete_create'),
    path('athlete/<int:pk>/update',
        views.AthleteUpdateView.as_view(success_url=reverse_lazy('team:all_athletes')), name='athlete_update'),

    
]