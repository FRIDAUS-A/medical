from django.shortcuts import render
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views

urlpatterns = [
	path("users", views.ProfileDetail.as_view())
]