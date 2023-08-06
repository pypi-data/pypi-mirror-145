#!/usr/bin/env python3
"""Setups urls for Chunky upload."""

__author__ = "Jaryd Rester"
__copyright__ = "2022-03-25"

# stdlib

# django
from django.urls import path


# local django
from chunky_upload.views import ChunkedUploadView

# thirdparty

urlpatterns = [
    path("upload/", ChunkedUploadView.as_view(), name="upload-view"),
    path("upload/<uuid:upload_id>/", ChunkedUploadView.as_view(), name="upload-view"),
]
