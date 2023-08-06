# -*- coding: utf-8 -*-

"""
BELA-dashboard web views
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from pathlib import Path

from django.shortcuts import render
from django.conf import settings

from belaweb.forms import ELANUploadForm
from belaweb.models import ELANFile
from belaweb.belaviz import visualize_bela
from belaweb.belaviz import BELA_DOCUMENTATION_OFFICIAL_URL
from belaweb.belaviz import BELA_DEFAULT_TITLE
from belaweb.belaviz import BELA_DASHBOARD_VERSION, BELA_DASHBOARD_BUILD
from belaweb.belaviz import BELA_SOURCE_REPO, BELA_ISSUE_URL
from belaweb.belaviz import SAFE_MODE, BELA_VERSION, EMPTY_BELA_VIZ
MEDIA_ROOT = Path(settings.MEDIA_ROOT)


# ------------------------------------------------------------------------------
# views
# ------------------------------------------------------------------------------

def bela_public(request):
    context = {'title': BELA_DEFAULT_TITLE,
               'BELA_VERSION': BELA_VERSION,
               'BELA_DASHBOARD_BUILD': BELA_DASHBOARD_BUILD,
               'BELA_DASHBOARD_VERSION': BELA_DASHBOARD_VERSION,
               'BELA_DOCUMENTATION_OFFICIAL_URL': BELA_DOCUMENTATION_OFFICIAL_URL,
               'BELA_SOURCE_REPO': BELA_SOURCE_REPO,
               'BELA_ISSUE_URL': BELA_ISSUE_URL,
               'SAFE_MODE': SAFE_MODE,
               'elanfile': None,
               'data': EMPTY_BELA_VIZ}
    form = None
    if request.method == "POST":
        form = ELANUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # build an ELANFile object in memory and visualise it
            # without saving to database
            elanfile_obj = ELANFile()
            elanfile_obj.content = form.cleaned_data['elanfile']
            elanfile_obj.original_name = form.cleaned_data['elanfile'].name
            visualize_bela(elanfile_obj, context)
    if form is None:
        form = ELANUploadForm()
    context['form'] = form
    return render(request, 'belaweb/bela_public.html', context)
