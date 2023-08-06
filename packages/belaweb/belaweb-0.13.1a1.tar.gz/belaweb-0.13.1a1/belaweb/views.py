# -*- coding: utf-8 -*-

"""
BELA-dashboard web views
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

import logging
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings

from sunshine.common import log_add, log_delete
from .forms import ELANUploadForm
from .models import ELANFile
from .apps import BELA_DASHBOARD_VERSION, BELA_DASHBOARD_BUILD
from .belaviz import BELA_VERSION, BELA_DEFAULT_TITLE, SAFE_MODE
from .belaviz import BELA_DOCUMENTATION_OFFICIAL_URL
from .belaviz import BELA_DOCUMENTATION_URL
from .belaviz import BELA_DOCUMENTATION_USERNAME, BELA_DOCUMENTATION_PASSWORD
from .belaviz.common import visualize_bela, visualize_bela_lex
from .belaviz.common import visualize_langmix_bar
MEDIA_ROOT = Path(settings.MEDIA_ROOT)


def __make_bela_view_context():
    return {'title': BELA_DEFAULT_TITLE,
            'BELA_VERSION': BELA_VERSION,
            'BELA_DASHBOARD_BUILD': BELA_DASHBOARD_BUILD,
            'BELA_DASHBOARD_VERSION': BELA_DASHBOARD_VERSION,
            'BELA_DOCUMENTATION_OFFICIAL_URL': BELA_DOCUMENTATION_OFFICIAL_URL,
            'BELA_DOCUMENTATION_URL': BELA_DOCUMENTATION_URL,
            'BELA_DOCUMENTATION_USERNAME': BELA_DOCUMENTATION_USERNAME,
            'BELA_DOCUMENTATION_PASSWORD': BELA_DOCUMENTATION_PASSWORD,
            'SAFE_MODE': SAFE_MODE}


# ------------------------------------------------------------------------------
# views
# ------------------------------------------------------------------------------

@login_required()
def bela_view_file(request, module="bela", username="", filename=""):
    context = __make_bela_view_context()
    if not username or not filename:
        return render(request, 'sunshine/404.html')
    elif username != request.user.username:
        return render(request, 'sunshine/403.html')
    elanfile = ELANFile.objects.filter(created_by__username=username, content=f'{module}/{username}/{filename}')
    if not elanfile.exists():
        return render(request, 'sunshine/404.html')
    else:
        # analyse an ELAN file
        elanfile_obj = elanfile.get()
        if elanfile_obj.original_name.lower().endswith(".eaf"):
            visualize_bela(elanfile_obj, context)
            return render(request, 'belaweb/bela_visual.html', context)
        elif elanfile_obj.original_name.lower().endswith(".lex.json"):
            visualize_bela_lex(elanfile_obj, context)
            return render(request, 'belaweb/bela_lexicon.html', context)
        elif elanfile_obj.original_name.lower().endswith('.bar.json'):
            visualize_langmix_bar(elanfile_obj, context)
            return render(request, 'belaweb/bela_langbars.html', context)
        else:
            return render(request, 'belaweb/format_error.html')


@login_required
def bela_delete_file(request, module="bela", username="", filename=""):
    if not username or not filename:
        return render(request, 'sunshine/404.html')
    elif username != request.user.username:
        return render(request, 'sunshine/403.html')
    elanfile = ELANFile.objects.filter(created_by__username=username, content=f'{module}/{username}/{filename}')
    if not elanfile.exists():
        return render(request, 'sunshine/404.html')
    else:
        elanfile = elanfile.first()
        logging.getLogger(__name__).warning(f'Deleting {module}/{username}/{filename}')
        log_delete(request, elanfile,
                   change_message=f"Deleted associated file: {elanfile.content.name} | uploaded name: {elanfile.original_name}")
        elanfile.delete()
        # proceed to delete file
        return redirect(bela_home)


@login_required()
def bela_home(request):
    form = None
    context = __make_bela_view_context()
    if request.method == "POST":
        form = ELANUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # try to build a model and save it ...
            elanfile = ELANFile()
            elanfile.content = form.cleaned_data['elanfile']
            elanfile.original_name = form.cleaned_data['elanfile'].name
            elanfile.created_by = request.user
            elanfile.save()
            log_add(request, elanfile)
    if form is None:
        form = ELANUploadForm()
    # list all accessible ELAN files
    context.update({
        'form': form,
        'elanfiles': ELANFile.objects.filter(created_by=request.user).order_by('-created_at')})
    return render(request, 'belaweb/home.html', context)
