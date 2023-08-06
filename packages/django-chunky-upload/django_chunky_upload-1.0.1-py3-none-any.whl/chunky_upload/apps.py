#!/usr/bin/env python3
"""Defines the AppConfig for the chunked_upload pluggable app."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-23"

# stdlib

# django
from django.apps import AppConfig

# local django

# thirdparty


class ChunkedUploadConfig(AppConfig):
    name = "chunky_upload"
    verbose_name = "Chunky Upload"
    default_auto_field = "django.db.models.BigAutoField"
