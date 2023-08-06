#!/usr/bin/env python

from pathlib import Path


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("VERSION.txt", "r") as v:
    version = v.read().strip()

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


download_url = "https://github.com/Vader19695/django-chunky-upload/tarball/%s"

setup(
    name="django-chunky-upload",
    packages=[
        "chunky_upload",
        "chunky_upload.migrations",
        "chunky_upload.management",
    ],
    version=version,
    description=(
        "Upload large files to Django in multiple chunks, with the "
        "ability to resume if the upload is interrupted."
    ),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Jaryd Rester",
    author_email="pypi@jarydrester.com",
    url="https://github.com/Vader19695/django-chunky-upload",
    download_url=download_url % version,
    python_requires=">=3.7",
    install_requires=[],
    license="MIT-Zero",
)
