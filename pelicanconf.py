#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jelle Smet'
SITENAME = u'http://smetj.net'
SITEURL = 'file:///home/smetj/projects/github/smetj.net/output'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'


THEME = '/home/smetj/Apps/pelican-themes/bootstrap2'
GITHUB_URL = 'http://github.com/smetj/'

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None

# Blogroll
# LINKS =  (('Pelican', 'http://getpelican.com/'),
#           ('Python.org', 'http://python.org/'),
#           ('Jinja2', 'http://jinja.pocoo.org/'),
#           ('You can modify those links in your config file', '#'),)
LINKS = None
PDF_GENERATOR = True
STATIC_PATHS = [
    'pics',
    ]
# Social widget
SOCIAL = (('twitter', 'http://twitter.com/smetj'),
          ('github', 'http://github.com/smetj'),)

DEFAULT_PAGINATION = 4
FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# FEED_ATOM = None

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
