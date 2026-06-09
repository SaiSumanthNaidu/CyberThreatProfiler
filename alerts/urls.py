from django.urls import path
from . import views

urlpatterns = [

    path('', views.alert_list, name='alerts'),

    path('add/', views.add_alert, name='add_alert'),

    path('edit/<int:id>/', views.edit_alert, name='edit_alert'),

    path('delete/<int:id>/', views.delete_alert, name='delete_alert'),

]