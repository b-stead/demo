from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name = 'data-viz'
urlpatterns = [
    path('', views.home, name='home'),
    path('demo1/', views.demo1, name='demo1'),
    path('demo2/', views.demo2, name='demo2'),
    path('demo3/', views.demo3, name='demo3'),
    
]