from django.contrib import admin
from django.urls import path, include
from .views import ForecastView

urlpatterns = [
    path("forecast", ForecastView.as_view(), name="forecast"),
]
