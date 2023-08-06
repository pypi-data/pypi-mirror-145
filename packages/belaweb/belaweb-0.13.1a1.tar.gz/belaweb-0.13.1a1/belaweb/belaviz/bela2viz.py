# -*- coding: utf-8 -*-

"""
BELA-dashboard visualizer for BELA-con version 2.x
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

import logging
from collections import defaultdict as dd

from bela import KNOWN_LANGUAGE_CLASSES
from bela import Bela2
from bela.lex import CorpusLexicalAnalyser

from blipleo.colors import to_color_list
from .langmixviz import LanguageTimeline
try:
    from belaweb.models import BELALexicalEntry
    __DB_AVAILABLE = True
except Exception:
    __DB_AVAILABLE = False


def build_language_color_map(language_set):
    languages = list(language_set)
    colors = to_color_list(languages, reuse_lastcolor=True)
    lang_color_map = {l: c if l not in KNOWN_LANGUAGE_CLASSES else '#999999' for l, c in zip(languages, colors)}
    return lang_color_map


def make_language_chart_json(lang_dur_map, color_map):
    language_list = [(k, v) for k, v in lang_dur_map.items()]
    language_list.sort(key=lambda x: (x[0] not in KNOWN_LANGUAGE_CLASSES, x[1]))
    langs = []
    durations = []
    for lang, dur in reversed(language_list):
        langs.append(lang)
        durations.append(round(dur, 2))
    colors = [color_map[l] for l in langs]
    return {
        'languages': langs,
        'durations': durations,
        'colors': colors,
        'all': [{'text': lang,
                 'duration': dur,
                 'color': color} for lang, dur, color in zip(langs, durations, colors)]
    }


def make_bela_language_chart_json(bela2_obj, color_map):
    ''' Calculate language chart stats '''
    lang_dur_map = dd(int)
    for tier in bela2_obj.tiers():
        if tier.tier_class == "Language":
            for ann in tier:
                if ann.duration is not None:
                    lang_dur_map[ann.value] += ann.duration
                elif ann.ref.duration is not None:
                    lang_dur_map[ann.value] += ann.ref.duration
    return make_language_chart_json(lang_dur_map, color_map)


def visualise_chatlog(bela2_obj, color_map, turn_starts, turn_takes):
    utterances = []
    max_length = 0
    for tier in bela2_obj.tiers():
        if tier.tier_class == "Utterance":
            for u in tier:
                is_error = u.errors is not None and len(u.errors) > 0
                tier_person = bela2_obj.person_map[tier.participant]
                ulength = 0
                chunks = []
                if u.chunks:
                    for child in u.chunks:
                        ulength += child.duration
                        # if not child.value or not child.value.strip():
                        #     child.errors.append("Empty chunk")
                        # elif not child.language:
                        #     if child.errors is None:
                        #         child.errors = []
                        #     child.errors.append("Language tag not found")
                        chunk_json = {
                            'text': child.value,
                            'language': child.language,
                            'color': color_map[child.language] if child.language else '',
                            'from_ts': child.from_ts.sec,
                            'to_ts': child.to_ts.sec,
                            'errors': child.errors
                        }
                        is_error = is_error or (child.errors is not None and len(child.errors) > 0)
                        chunks.append(chunk_json)
                if ulength == 0:
                    # no chunk -- probably error?
                    ulength = u.duration
                utterance_json = {
                    'text': u.value,
                    'length': ulength,
                    'chunks': chunks,
                    'speaker': tier_person.code,
                    'speaker_name': tier_person.name,
                    'is_baby': tier_person.name == "Baby",
                    'from_ts': u.from_ts.sec,
                    'errors': u.errors,
                    'is_error': is_error,
                    'is_turnA': u.ID in turn_starts,
                    'is_turnB': u.ID in turn_takes,
                    'trans': u.translation if u.translation else ''
                }
                if ulength > max_length:
                    max_length = ulength
                utterances.append(utterance_json)
    try:
        utterances.sort(key=lambda x: x['from_ts'])
    except Exception:
        if utterances:
            utterances[0]['errors'].append("Could not construct a timeline for corrupted transcription")
        pass
    speaking = ''
    for idx, chatline in enumerate(utterances):
        chatline['rduration'] = chatline['length'] * 100 / max_length
        chatline['rremainder'] = 100 - chatline['length'] * 100 / max_length
        if speaking != chatline['speaker']:
            chatline['is_continue'] = False
            speaking = chatline['speaker']
        else:
            chatline['is_continue'] = True
        for chunk in chatline['chunks']:
            try:
                chunk['rduration'] = (chunk['to_ts'] - chunk['from_ts']) * 100 / max_length
            except:
                chunk['errors'].append("Could not calculate chunk duration for corrupted annotations")
                chunk['rduration'] = 1
    return utterances


def make_people_json(bela2_obj, color_map, turn_map):
    people = []
    for person in bela2_obj.persons:
        duration = 0
        utterance_count = 0
        word_count = 0
        if person.utterances:
            for ann in person.utterances:
                duration += ann.duration
                utterance_count += 1
        lang_dur_map = dd(int)
        if person['Chunk']:
            for ann in person['Chunk']:
                if ann.words:
                    word_count += len(ann.words)
        if person['Language']:
            for ann in person['Language']:
                if ann.duration is not None:
                    lang_dur_map[ann.value] += ann.duration
                elif ann.ref is not None and ann.ref.duration is not None:
                    lang_dur_map[ann.value] += ann.ref.duration
        if utterance_count > 0:
            MLU = round(word_count / utterance_count, 3)
        else:
            MLU = 'N/A'
        person_json = {
            'name': person.name,
            'code': person.code,
            'duration': round(duration, 3),
            'languages': make_language_chart_json(lang_dur_map, color_map),
            'tiers': person.tier_classes,
            'utterance_count': utterance_count,
            'wordcount': word_count,
            'MLU': MLU,
            'turns': 0 if person.code not in turn_map else turn_map[person.code]
        }
        people.append(person_json)
    people.sort(key=lambda x: -x['utterance_count'])
    return people


def _query_custom_lang_lex_map():
    if not __DB_AVAILABLE:
        return []
    # mock-data
    # _le_map = {'English': {'meow', 'tsk'}, 'Mandarin': {'error'}}
    try:
        entries = BELALexicalEntry.objects.only('text', 'language')
    except Exception:
        logging.getLogger(__name__).exception("Could not access custom lexical entry database")
        entries = []
    _le_map = dd(set)
    for e in entries:
        _le_map[e.language].add(e.text)
    return _le_map


def analyser_lexical(bela2_obj, source='', auto_compute=True):
    analyser = CorpusLexicalAnalyser(
        lang_lex_map=_query_custom_lang_lex_map(),
        word_only=False,
        lemmatizer=True)
    for person in bela2_obj.persons:
        if person['Utterance']:
            for u in person['Utterance']:
                if u.chunks:
                    for ru in u.chunks:
                        analyser.add(ru.value, ru.language, source=source, speaker=person.code)
                else:
                    u.errors.append(f"ERROR: Utterance with no chunk")
                    analyser.add(u.value, u.language, source=source, speaker=person.code)
    if auto_compute:
        analyser.analyse()
    return analyser


def count_errors(bela2_obj):
    errors = len(bela2_obj.errors) if bela2_obj.errors else 0
    for person in bela2_obj.persons:
        if person.utterances:
            for u in person.utterances:
                if u.errors:
                    errors += len(u.errors)
    return errors


def visualize_bela2(elan, eaf_path=":memory:"):
    bela2_obj = Bela2.from_elan(elan, eaf_path=eaf_path)
    language_set = bela2_obj.get_language_set()
    color_map = build_language_color_map(language_set)
    lexicon = analyser_lexical(bela2_obj)
    lexicon_list = lexicon.to_dict()
    for l in lexicon_list:
        if 'errors' in l['stats'] and len(l['stats']['errors']):
            if bela2_obj.errors is None:
                bela2_obj.errors = []
            for e in l['stats']['errors']:
                bela2_obj.errors.append(f"Lexicon warning: {e} (Refresh in a minute to try again)")
    lexstats = {
        'stats': lexicon_list,
        'all': lexicon.profiles['ALL'].to_dict(),
        'sorting_mode': '', 'message': '', 'table_mode': True
        }
    turn_starts = set()
    turn_takes = set()
    turn_map = dd(int)
    try:
        for u, nu in bela2_obj.find_turns():
            turn_starts.add(u.ID)
            turn_takes.add(nu.ID)
            turn_map[u.person.code] += 1
    except Exception:
        bela2_obj.errors.append("Could not calculate turns")
    data = {
        'anncount': bela2_obj.count_chunks(),  # how many chunks
        'sentcount': bela2_obj.count_sents(),  # how many utterances
        'languages': make_bela_language_chart_json(bela2_obj, color_map),  # language stats
        'people': make_people_json(bela2_obj, color_map, turn_map),  # people's stats
        'chatlog': visualise_chatlog(bela2_obj, color_map, turn_starts, turn_takes),  # all utterances
        'errors': bela2_obj.errors,
        'error_count': count_errors(bela2_obj),
        'langmix_bar': LanguageTimeline.from_langmix(bela2_obj.to_language_mix().to_dict(), color_map=color_map).data,
        'lexstats': lexstats,
        'table_mode': False,
        'show_freq': False,
        'error_only': False,
        'turns_only': False,
        'belacon_version': 2.0,
        'special_lex_only': True,
        'show_translation': True
    }
    return data
