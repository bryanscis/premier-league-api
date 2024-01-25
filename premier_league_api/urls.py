"""
URL configuration for premier_league_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from premier_league_api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include([
        path("add-managers/", views.add_managers),
        path("add-fixtures/", views.add_fixtures),
        path("add-players/", views.add_players),
        path("teams/", views.get_teams),
        path("managers/", views.get_managers),
        path("fixtures/", views.get_fixtures),
        path("players/", views.get_players),
    ])),
]
