# -*- coding: utf-8 -*-

"""
BELA-dashboard upload form
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from django import forms


class ELANUploadForm(forms.Form):
    elanfile = forms.FileField(label="ELAN File",
                               widget=forms.FileInput(attrs={'accept': '.eaf, .bar.json, .lex.json'}))
