#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jelle Smet'
SITENAME = u'Project site of Jelle Smet'
#SITESUBTITLE = u'</br>Curiosity driven development. Python - Monitoring - Metrics - Events - Automation - Infrastructure.'
SITEURL = 'http://smetj.net'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'


THEME = '/home/smetj/data/projects/github/pelican-bootstrap3/'
BOOTSTRAP_THEME = 'flatly'
GITHUB_USER = 'smetj'

PLUGIN_PATH = '/home/smetj/data/projects/github/pelican-plugins'
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

DISPLAY_TAGS_ON_SIDEBAR = False
LINKS = None
PDF_GENERATOR = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
STATIC_PATHS = [
    'pics',
    'robots.txt'
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
RELATIVE_URLS = True
PYGMENTS_STYLE = "friendly"
GITHUB_SKIP_FORK = True