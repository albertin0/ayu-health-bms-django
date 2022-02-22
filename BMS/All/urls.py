from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("view/movie/<id>", views.view_movie, name='view_movie'),
    path("add/movie", views.add_movie, name='add_movie'),
    path('view/seats', views.view_seats, name='view_seats'),
    path('save/layout', views.save_layout, name='save_layout')
]