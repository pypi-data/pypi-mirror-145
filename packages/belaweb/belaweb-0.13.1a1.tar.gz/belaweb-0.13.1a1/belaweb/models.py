# -*- coding: utf-8 -*-

"""
BELA-dashboard model
"""

# This code is a part of belaweb system: https://github.com/letuananh/belaweb
# :developer: Le Tuan Anh <tuananh.ke@gmail.com>
# :license: MIT, see LICENSE for more details.

import logging
import uuid
from pathlib import Path
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


MEDIA_ROOT = Path(settings.MEDIA_ROOT)


def getLogger():
    return logging.getLogger(__name__)


def setup_filename(instance, filename):
    # suffix = Path(filename).suffix
    return f"bela/{instance.created_by.username}/{str(uuid.uuid4())}"


class ELANFile(models.Model):
    content = models.FileField(upload_to=setup_filename)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    original_name = models.CharField(max_length=200, blank=False)
    updated_by = models.ForeignKey(User, null=True, related_name="updated_by", on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, related_name="created_by", on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.original_name} - {self.content}"

    class Meta:
        verbose_name = 'BELA transcript'
        verbose_name_plural = 'BELA transcripts'


class BELALexicalEntry(models.Model):
    text = models.CharField(max_length=100, blank=False)
    language = models.CharField(max_length=100, blank=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name="ble_updated_by", on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, related_name="ble_created_by", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'lexical entry'
        verbose_name_plural = 'lexical entries'
        unique_together = ('text', 'language')
        indexes = [
            models.Index(fields=['text', 'language']),
        ]

    def __str__(self):
        return f"[{self.language}]/{self.text}"


@receiver(pre_delete, sender=ELANFile)
def elanfile_cleanup(sender, instance, **kwargs):
    try:
        if instance is not None and instance.content is not None:
            elanfile_path = MEDIA_ROOT / instance.content.name
            if elanfile_path.exists():
                instance.content.delete(False)
            getLogger().info(f"Deleted ELAN file: {elanfile_path}")
    except Exception:
        getLogger().exception(f"Could not clean up file {instance}")
