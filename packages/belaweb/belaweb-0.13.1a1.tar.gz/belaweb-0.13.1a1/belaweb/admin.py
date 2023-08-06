# -*- coding: utf-8 -*-

"""
BELA-dashboard admin
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

from django.contrib import admin

from .models import ELANFile, BELALexicalEntry


@admin.register(ELANFile)
class ELANFileAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'created_by', 'created_at', 'content', 'notes')
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'content')
    search_fields = ('original_name', 'notes', 'content')
    list_filter = ('created_by',)

    def save_model(self, request, obj, form, change):
        if change:
            obj.created_by = request.user
        else:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BELALexicalEntry)
class BELALexicalEntryAdmin(admin.ModelAdmin):
    list_display = ('text', 'language', 'created_by', 'updated_at')
    list_filter = ('language',)
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

    def save_model(self, request, obj, form, change):
        if change:
            obj.created_by = request.user
        else:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
