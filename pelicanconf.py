#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jelle Smet'
SITENAME = u'Project site of Jelle Smet'
#SITESUBTITLE = u'</br>Curiosity driven development. Python - Monitoring - Metrics - Events - Automation - Infrastructure.'
SITEURL = 'http://smetj.net'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'


#THEME = '/home/smetj/projects/github/pelican-themes/bootstrap2'
THEME = '/home/smetj/projects/github/pelican-themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'flatly'
GITHUB_URL = 'http://github.com/smetj/'
GITHUB_USER = 'smetj'

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None

# Blogroll
# LINKS =  (('Pelican', 'http://getpelican.com/'),
#           ('Python.org', 'http://python.org/'),
#           ('Jinja2', 'http://jinja.pocoo.org/'),
#           ('You can modify those links in your config file', '#'),)

PLUGIN_PATH = '/home/smetj/projects/github/pelican-plugins'
PLUGINS = ['summary','sitemap']

SUMMARY_BEGIN_MARKER = "xxstart_summaryxx"
SUMMARY_END_MARKER = "xxend_summaryxx"

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'weekly'
    }
}

LINKS = None
PDF_GENERATOR = True
STATIC_PATHS = [
    'pics',
    ]
# Social widget
SOCIAL = (('twitter', 'http://twitter.com/smetj'),
          ('github', 'http://github.com/smetj'),)
DEFAULT_PAGINATION = 10
FEED_DOMAIN = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
FEED_ATOM = None
FEED_RSS = None
TAG_FEED = None
DISQUS_SITENAME = "smetj"
GOOGLE_ANALYTICS = "UA-40703057-1"
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
