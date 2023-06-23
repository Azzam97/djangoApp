from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('teams/new', views.new),
    path('create_team', views.create_team),
    path('teams/<int:id>', views.show),
    path('teams/<int:id>/edit', views.edit),
    path('teams/<int:id>/update_team', views.update_team),
    path('teams/<int:id>/delete', views.delete)
]