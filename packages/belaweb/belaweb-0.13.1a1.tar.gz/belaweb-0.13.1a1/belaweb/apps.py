# -*- coding: utf-8 -*-

"""
BELA-dashboard web config
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from django.apps import AppConfig
from belaweb.belaviz import BELA_DASHBOARD_VERSION
from belaweb.belaviz import BELA_DASHBOARD_BUILD
from belaweb.belaviz import BELA_DEFAULT_TITLE
from belaweb.belaviz import BELA_DEFAULT_TITLE_SHORT
from belaweb.belaviz.common import has_access_to_bela


class BelaWebConfig(AppConfig):
    name = 'belaweb'
    verbose_name = BELA_DEFAULT_TITLE
    version = BELA_DASHBOARD_VERSION
    version_build = BELA_DASHBOARD_BUILD
    sunshine_path = 'bela/'
    namespace = ''
    sunshine_menu = [
        ('belaweb_home',
         has_access_to_bela,
         BELA_DEFAULT_TITLE_SHORT,
         'fa-scroll',
         ['Systems'])
    ]
