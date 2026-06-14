from django.urls import path
from . import views

urlpatterns = [

    path('', views.threat_list, name='threats'),

    path('add/', views.add_threat, name='add_threat'),

    path('edit/<int:id>/', views.edit_threat, name='edit_threat'),

    path('delete/<int:id>/', views.delete_threat, name='delete_threat'),

    path('detail/<int:id>/', views.threat_detail, name='threat_detail'),

]