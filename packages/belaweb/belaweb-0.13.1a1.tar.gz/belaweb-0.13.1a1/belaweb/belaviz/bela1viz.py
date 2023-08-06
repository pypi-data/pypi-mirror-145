# -*- coding: utf-8 -*-

"""
BELA-dashboard visualizer for BELA-con version 1.x
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from bela import tokenize
from bela import KNOWN_LANGUAGE_CLASSES
from bela.bela1 import Bela1
from bela.bela1 import build_utterances_json
from bela.lex import CorpusLexicalAnalyser

from blipleo.colors import to_color_list
from .langmixviz import LanguageTimeline
from .bela2viz import _query_custom_lang_lex_map


def build_language_color_map(sents):
    language_set = set()
    for u in sents:
        for chunk in u:
            language_set.add(chunk['language'])
    languages = list(language_set)
    colors = to_color_list(languages, reuse_lastcolor=True)
    lang_color_map = {l: c if l not in KNOWN_LANGUAGE_CLASSES else '#999999' for l, c in zip(languages, colors)}
    return lang_color_map


def make_language_chart_json(language_list, color_map):
    ''' Transform a list of (lang,dur) into language representable list '''
    langs = []
    durations = []
    language_list.sort(key=lambda x: (x[0] not in KNOWN_LANGUAGE_CLASSES, x[1]))
    for lang, dur in reversed(language_list):
        langs.append(lang)
        durations.append(dur)
    colors = [color_map[l] for l in langs]
    return {
        'languages': langs,
        'durations': durations,
        'colors': colors,
        'all': [{'text': lang,
                 'duration': dur,
                 'color': color} for lang, dur, color in zip(langs, durations, colors)]
    }


def visualise_chatlog(utterances, color_map):
    max_length = 0
    chatlog = []
    utterance_lengths = []
    utterances.sort(key=lambda x: (x[0]['tsfrom'],))
    for u in utterances:
        ulength = 0
        for chunk in u:
            ulength += chunk['tsto'] - chunk['tsfrom']
        if ulength > max_length:
            max_length = ulength
        utterance_lengths.append(ulength)
    speaking = ''
    for idx, u in enumerate(utterances):
        chatline = {'speaker': u[0]['speaker'],
                    'speaker_name': u[0]['speaker_name'],
                    'is_continue': True,
                    'chunks': [],
                    'rduration': utterance_lengths[idx] * 100 / max_length,
                    'rremainder': 100 - utterance_lengths[idx] * 100 / max_length,
                    'is_baby': u[0]['speaker_name'] == 'Baby',
                    'errors': [],
                    'is_turnA': False,
                    'is_turnB': False,
                    'trans': ''}  # bela v1 doesn't support translation
        if speaking != u[0]['speaker']:
            chatline['is_continue'] = False
            speaking = u[0]['speaker']
        for chunk in u:
            chunk_is_error = False
            chunk_relative_duration = (chunk['tsto'] - chunk['tsfrom']) * 100 / max_length
            vchunk = {'text': chunk['text'],
                      'language': chunk['language'],
                      'rduration': chunk_relative_duration,
                      'color': color_map[chunk['language']],
                      'errors': [],
                      'is_error': chunk_is_error}
            chatline['chunks'].append(vchunk)
        chatlog.append(chatline)
    return chatlog


def make_people_json(elan_dict, utterances, color_map):
    people = elan_dict['people']
    for person in people:
        if 'languages' in person:
            person['languages'] = make_language_chart_json(person['languages'], color_map)
    people.sort(key=lambda x: -x['utterance_count'])
    # count words & MLU
    for p in people:
        p['wordcount'] = 0
        p['utterance_count'] = 0
    people_map = {p['code'][0]: p for p in people}
    for u in utterances:
        p = people_map[u[0]['speaker']]
        p['utterance_count'] += 1
        for chunk in u:
            words = tokenize(chunk['text'], language=chunk['language'])
            chunk['words'] = words
            p['wordcount'] += len(words)
    for p in people:
        p['code'] = ', '.join(p['code'])
        p['turns'] = 0
        if p['utterance_count'] > 0:
            p['MLU'] = round(p['wordcount'] / p['utterance_count'], 3)
        else:
            p['MLU'] = 'N/A'
    return people


def analyser_lexical(bela1_obj, source='', auto_compute=True):
    analyser = CorpusLexicalAnalyser(lang_lex_map=_query_custom_lang_lex_map(), word_only=False)
    for _person_name, _utterances in bela1_obj.person_utterances.items():
        for u in _utterances:
            analyser.add(u.text, u.language, source=source, speaker=_person_name)
    if auto_compute:
        analyser.analyse()
    return analyser


def visualize_bela1(elan, eaf_path=":memory:"):
    elanplus = Bela1.from_elan(elan, eaf_path=eaf_path)
    sents = build_utterances_json(elanplus)
    color_map = build_language_color_map(sents)
    elan_dict = elanplus.to_dict()
    chatlog = visualise_chatlog(sents, color_map)
    lexicon = analyser_lexical(elanplus)
    lexstats = {
        'stats': lexicon.to_dict(),
        'all': lexicon.profiles['ALL'].to_dict(),
        'sorting_mode': '', 'message': '', 'table_mode': True
        }
    data = {
        'anncount': len(elanplus.csw),  # how many chunks
        'sentcount': len(sents),  # how many utterances
        'languages': make_language_chart_json(elan_dict['languages'], color_map),  # language stats
        'people': make_people_json(elan_dict, sents, color_map),  # people's stats
        'chatlog': chatlog,  # all utterances
        'errors': [],  # TODO - support errors in PILOT1,
        'error_count': -1,
        'langmix_bar': LanguageTimeline.from_langmix(elanplus.to_language_mix().to_dict(), color_map=color_map).data,
        'lexstats': lexstats,
        'error_only': False,
        'turns_only': False,
        'table_mode': False,
        'show_freq': False,
        'belacon_version': 1.0,
        'special_lex_only': True,
        'show_translation': True
    }
    return data
