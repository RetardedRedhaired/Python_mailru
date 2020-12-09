from django.urls import path

from homm3_creatures.views import CreatureView

urlpatterns = [
    path('api/', CreatureView.as_view()),
    path('api/<int:pk>', CreatureView.as_view()),
]