from django.urls import path
from . import views

urlpatterns = [

    path('', views.feed_list, name='feed'),

    path('add/', views.add_feed, name='add_feed'),

    path('edit/<int:id>/', views.edit_feed, name='edit_feed'),

    path('delete/<int:id>/', views.delete_feed, name='delete_feed'),

]