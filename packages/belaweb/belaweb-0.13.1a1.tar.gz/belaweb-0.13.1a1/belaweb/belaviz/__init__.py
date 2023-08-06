# -*- coding: utf-8 -*-

"""
BELA-dashboard visualization engine package
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from .bela1viz import visualize_bela1
from .bela2viz import visualize_bela2
from .common import visualize_bela
from .langmixviz import LanguageTimeline
from .common import SAFE_MODE
from bela import __version__ as BELA_VERSION
from belaweb.__version__ import BELA_DASHBOARD_VERSION, BELA_DASHBOARD_BUILD
from .common import BELA_DEFAULT_TITLE, BELA_DEFAULT_TITLE_SHORT
from .common import BELA_DOCUMENTATION_OFFICIAL_URL
from .common import BELA_DOCUMENTATION_URL
from .common import BELA_DOCUMENTATION_USERNAME
from .common import BELA_DOCUMENTATION_PASSWORD
from .common import BELA_SOURCE_REPO
from .common import BELA_ISSUE_URL
from .common import EMPTY_BELA_VIZ
from bela.lex import CorpusLexicalAnalyser

__all__ = ['visualize_bela',
           'visualize_bela1',
           'visualize_bela2',
           'LanguageTimeline',
           'BELA_VERSION', 'SAFE_MODE', 'EMPTY_BELA_VIZ',
           'BELA_DASHBOARD_VERSION', 'BELA_DASHBOARD_BUILD',
           'BELA_DEFAULT_TITLE', 'BELA_DEFAULT_TITLE_SHORT',
           'BELA_DOCUMENTATION_OFFICIAL_URL',
           'BELA_DOCUMENTATION_URL',
           'BELA_DOCUMENTATION_USERNAME',
           'BELA_DOCUMENTATION_PASSWORD',
           'BELA_SOURCE_REPO', 'BELA_ISSUE_URL',
           'CorpusLexicalAnalyser']
