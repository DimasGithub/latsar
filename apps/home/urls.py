# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views


app_name = 'dashboard'

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.RetributionCalulationViewSet.as_view(), name="hitung_retribusi"),
]