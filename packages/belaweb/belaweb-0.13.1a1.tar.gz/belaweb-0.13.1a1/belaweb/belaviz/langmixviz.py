# -*- coding: utf-8 -*-

"""
BELA-dashboard language timeline chart
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

import json
from collections import Counter
from blipleo.colors import to_color_list
from bela import KNOWN_LANGUAGE_CLASSES


class LanguageTimeline:
    def __init__(self, color_map=None):
        self.data = None
        self.color_map = color_map

    @property
    def chunks(self):
        return self.data

    def _process(self):
        # build language map
        languages = Counter()
        languages.update(x[0] if x[0] else '' for x in self.data['chunks'])
        if self.color_map is None:
            colors = to_color_list(languages, reuse_lastcolor=True)
            self.color_map = {l: c if l not in KNOWN_LANGUAGE_CLASSES else '#999999' for l, c in zip(languages, colors)}
        for chunk in self.data['chunks']:
            chunk_lang = chunk[0] if chunk[0] else ''
            chunk[1] = chunk[1] * 100 / self.data['length']
            chunk.append(self.color_map[chunk_lang] if chunk_lang in self.color_map else '#FF0000')
        self.data['rel_length'] = sum(chunk[1] for chunk in self.data['chunks'])
        return self.data

    @staticmethod
    def from_langmix(data, color_map=None):
        langmix_viz = LanguageTimeline(color_map=color_map)
        langmix_viz.data = data
        langmix_viz._process()
        return langmix_viz

    @staticmethod
    def from_str(text, color_map=None):
        data = json.loads(text)
        bars = []
        for lm in data:
            lm_timeline = LanguageTimeline.from_langmix(lm, color_map=color_map)
            bars.append(lm_timeline)
        return bars

    @staticmethod
    def from_bytes(b, color_map=None):
        return LanguageTimeline.from_str(b.decode('utf-8'))
    
    @staticmethod
    def read(filepath, color_map=None):
        ''' Read language timeline from a JSON file '''
        return LanguageTimeline.from_str(filepath.read_text())
