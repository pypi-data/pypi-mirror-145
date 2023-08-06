#!/usr/bin/env python3
# coding=utf8

from setuptools import setup, find_packages
from sonofman import som_version

somversion = som_version.SomVersion()

# noinspection PyBroadException
try:
    f = open('README.rst')
    long_desc = f.read()
except Exception:
    long_desc = 'Bible multi languages, free, offline, no advertising, in English, French, Italian, Spanish, Portuguese, German (partially) for ' \
                'Terminal. Easy to use with quick searches, parables, articles, cross references, favorites, history'

setup(
    name=somversion.app_name,
    version=somversion.app_version,
    author=somversion.author,
    author_email=somversion.author_email,
    description='Bible multi languages, free, offline, no advertising, in English, French, Italian, Spanish, Portuguese, German (partially) for '
                'Terminal. Easy to use with quick searches, parables, articles, cross references, favorites, history',
    entry_points={"console_scripts": ["sonofman=sonofman.som_main:main", "som=sonofman.som_main:main"]},
    license=somversion.licence,
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    keywords="bible, multi, bible multi, biblia, bíblia, bibbia, bibel, reading, terminal, ncurses, CLI, english, français, italiano, española, "
             "german, portuguese, python, mac, linux, raspberry, arm, sonofman, jesus",
    packages=find_packages(),
    install_requires=["pyperclip"],
    include_package_data=True,
    url='https://gitlab.com/hotlittlewhitedog/BibleMultiTheSonOfMan',
    project_urls={
        "Bug Tracker": somversion.issue,
        "Documentation": somversion.url,
        "Source Code": somversion.url
    },
    zip_safe=False,
    classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Education",
            "Intended Audience :: Religion",
            "Programming Language :: Python",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Topic :: Religion"],
)
