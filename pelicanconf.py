#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jelle Smet'
SITENAME = u'Project site of Jelle Smet'
SITEURL = 'https://smetj.net'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'

BANNER = '/pics/banner.png'
BANNER_SUBTITLE = 'Technical musings of an automator, developer and systems engineer.'
BOOTSTRAP_FLUID = False

THEME = '/home/smetj/data/projects/github/pelican-themes/pelican-bootstrap3'
# BOOTSTRAP_THEME = 'flatly'
BOOTSTRAP_THEME = 'journal'
# GITHUB_USER = 'smetj'
# GITHUB_SKIP_FORK = True
CUSTOM_CSS = 'css/custom.css'
PLUGIN_PATHS = [
    '/home/smetj/data/projects/github/pelican-plugins'
]
PLUGINS = [
    'summary',
    'sitemap',
    'pelican_gist',
    'simple_footnotes',
    'i18n_subsites'
]
BOOTSTRAP_NAVBAR_INVERSE = True

SUMMARY_BEGIN_MARKER = "__start_summary__"
SUMMARY_END_MARKER = "__end_summary__"

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
    'robots.txt',
    ]

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/smetj'),
          ('github', 'https://github.com/smetj'),)
TRAVIS = [
    {"name": "Wishbone", "id": "smetj/wishbone", "github": "smetj/wishbone"},
    {"name": "AMQP input", "id": "wishbone-modules/wishbone-input-amqp", "github": "wishbone-modules/wishbone-input-amqp"},
    {"name": "AMQP output", "id": "wishbone-modules/wishbone-output-amqp", "github": "wishbone-modules/wishbone-output-amqp"},
    {"name": "Azure Q Storage In", "id": "wishbone-modules/wishbone-input-azure_queue_storage", "github": "wishbone-modules/wishbone-input-azure_queue_storage"},
    {"name": "Azure Q Storage Out", "id": "wishbone-modules/wishbone-output-azure_queue_storage", "github": "wishbone-modules/wishbone-output-azure_queue_storage"},
    {"name": "HTTP input", "id": "wishbone-modules/wishbone-input-httpserver", "github": "wishbone-modules/wishbone-input-httpserver"},
    {"name": "HTTP output", "id": "wishbone-modules/wishbone-output-http", "github": "wishbone-modules/wishbone-output-http"},
    {"name": "Twitter output", "id": "wishbone-modules/wishbone-output-twitter", "github": "wishbone-modules/wishbone-output-twitter"},
]
DEFAULT_PAGINATION = 10
FEED_DOMAIN = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
FEED_ATOM = None
FEED_RSS = None
TAG_FEED = None
DISQUS_SITENAME = "smetj"
DISQUSURL = 'http://smetj.net'
GOOGLE_ANALYTICS = "UA-40703057-1"
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
PYGMENTS_STYLE = "manni"

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
