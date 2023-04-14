from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('consumers', views.Consumers.as_view()),
]
