# -*- coding: utf-8 -*-

"""
BELA-dashboard public URL mapping
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.bela_public),
    path('home/', views.bela_public),
    path('gui/', views.bela_public, name='belaweb_public'),
]
