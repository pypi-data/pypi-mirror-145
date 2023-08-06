# -*- coding: utf-8 -*-

"""
BELA visualization engine - common functions
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

import logging
import io
import json

from speach import elan

from django.conf import settings
from .bela1viz import visualize_bela1
from .bela2viz import visualize_bela2
from .langmixviz import LanguageTimeline

try:
    SAFE_MODE = elan.SAFE_MODE
except Exception:
    SAFE_MODE = False
from bela import __version__ as BELA_VERSION
BELA_DEFAULT_TITLE = getattr(settings, "BELA_DEFAULT_TITLE", "BELA Dashboard")
BELA_DEFAULT_TITLE_SHORT = getattr(settings, "BELA_DEFAULT_TITLE_SHORT", "BELA")
# This should be used on the public service because it points to
# stable, version-controlled copy of the BELA convention (for reproducibility of studies)
# Although the official URL is overridable in sunshine settings files
# it should not be changed without a strong reason
BELA_DOCUMENTATION_OFFICIAL_URL = getattr(settings, "BELA_DOCUMENTATION_OFFICIAL_URL", "https://blipntu.github.io/belacon/")
# This URL will be used for staff dashboard version of belaweb
# - to test out a new belacon that is not stable enough yet for the public
# - the study uses a specific (older?) version of the belacon
BELA_DOCUMENTATION_URL = getattr(settings, "BELA_DOCUMENTATION_URL", "https://blipntu.github.io/belacon/")
# Github page should not require login
BELA_DOCUMENTATION_USERNAME = getattr(settings, "BELA_DOCUMENTATION_USERNAME", "")
BELA_DOCUMENTATION_PASSWORD = getattr(settings, "BELA_DOCUMENTATION_PASSWORD", "")
BELA_SOURCE_REPO = getattr(settings, "BELA_SOURCE_REPO", "https://github.com/letuananh/belaweb")
BELA_ISSUE_URL = getattr(settings, "BELA_ISSUE_URL", "https://github.com/letuananh/belaweb/issues")
BELA_USER_GROUP = getattr(settings, "BELA_USER_GROUP", "Corpus")


def is_nested(elan):
    for tier in elan:
        if tier.children:
            return True
    return False


EMPTY_BELA_VIZ = {
    'anncount': -1,  # how many chunks
    'sentcount': -1,  # how many utterances
    'languages': {},  # language stats
    'people': {},  # people's stats
    'chatlog': {},  # all utterances
    'errors': [],
    'error_count': -1,
    'langmix_bar': {},
    'lexstats': {
        'stats': {}, 'all': {},
        'sorting_mode': '', 'message': '', 'table_mode': True},
    'table_mode': False,
    'show_freq': False,
    'error_only': False,
    'turns_only': False,
    'belacon_version': BELA_VERSION,
    'special_lex_only': False,
    'show_translation': True
}


def has_access_to_bela(req):
    try:
        return req.user.is_superuser or req.user.groups.filter(name=BELA_USER_GROUP).exists()
    except Exception:
        return False


def visualize_bela(elanfile_obj, context):
    try:
        eaf = elan.parse_eaf_stream(io.BytesIO(elanfile_obj.content.read()))
        if not is_nested(eaf):
            data = visualize_bela1(eaf, eaf_path=elanfile_obj.original_name)
        else:
            data = visualize_bela2(eaf, eaf_path=elanfile_obj.original_name)
    except Exception:
        logging.getLogger(__name__).exception(f"Could not parse BELA file {elanfile_obj.original_name} ({elanfile_obj.original_name})")
        data = EMPTY_BELA_VIZ
    __view_context = {
        'title': f'{BELA_DEFAULT_TITLE_SHORT} | {elanfile_obj.original_name}',
        'elanfile': elanfile_obj,  # database object
        'data': data
    }
    if context is not None:
        context.update(__view_context)
    return __view_context


def visualize_bela_lex(elanfile_obj, context):
    _lexstats = json.load(io.BytesIO(elanfile_obj.content.read()))
    __view_context = {
        'elanfile': elanfile_obj,
        'lexstats': _lexstats
    }
    if context is not None:
        context.update(__view_context)
    return __view_context


def visualize_langmix_bar(elanfile_obj, context):
    langmix_viz = LanguageTimeline.from_bytes(elanfile_obj.content.read())
    bars = [x.data for x in langmix_viz]
    __view_context = {
        'elanfile': elanfile_obj,
        'bar_data': bars}
    if context is not None:
        context.update(__view_context)
    return __view_context
