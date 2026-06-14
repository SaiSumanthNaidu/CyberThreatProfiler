from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path(
        'refresh-threats/',
        views.refresh_threats,
        name='refresh_threats'
    ),
]