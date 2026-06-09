from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('threats/', include('nlp_engine.urls')),
    path('alerts/', include('alerts.urls')),
    path('feed/', include('collector.urls')),
    path('posts/', include('posts.urls')),
]