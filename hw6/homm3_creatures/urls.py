from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from homm3_creatures.views import CreatureView, home, login

urlpatterns = [
    path('', home, name='home'),
    path('api/', CreatureView.as_view()),
    path('api/<int:pk>', CreatureView.as_view()),
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social_auth/', include('social_django.urls', namespace='social')),
]