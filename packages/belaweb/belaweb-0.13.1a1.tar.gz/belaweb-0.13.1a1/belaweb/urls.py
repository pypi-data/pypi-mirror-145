# -*- coding: utf-8 -*-

"""
BELA-dashboard URL mapping
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from django.urls import path

from . import views
from .public import views as public_views

urlpatterns = [
    path('', views.bela_home),
    path('home/', views.bela_home, name='belaweb_home'),
    path('gui/', public_views.bela_public, name='belaweb_public'),
    path('check/', views.bela_view_file, name='belaweb_visualize'),
    path('check/<slug:module>/<slug:username>/<uuid:filename>', views.bela_view_file, name='belaweb_visualize'),
    path('delete/', views.bela_delete_file, name='belaweb_deletefile'),
    path('delete/<slug:module>/<slug:username>/<uuid:filename>', views.bela_delete_file, name='belaweb_deletefile'),
]
