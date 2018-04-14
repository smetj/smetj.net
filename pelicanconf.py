#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

ABOUT_ME = '''
Do you want help with API integrations, automation, event processing or monitoring?
</br><font color="EB6864"><a href="https://www.linkedin.com/in/jelle-smet-594a907b/">Get in touch and let's talk!</a></font>
'''

AUTHOR = u'Jelle Smet'
BANNER = '/pics/banner.png'
BANNER_SUBTITLE = 'Technical musings of an automator, developer and systems engineer.'

BOOTSTRAP_FLUID = False
BOOTSTRAP_NAVBAR_INVERSE = True
BOOTSTRAP_THEME = 'journal'

CATEGORY_FEED_ATOM = None

DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 10

DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISPLAY_TAGS_ON_SIDEBAR = False

DISQUS_SITENAME = "smetj"
DISQUSURL = 'https://smetj.net'
DISQUS_DISPLAY_COUNTS = False

FEED_ALL_ATOM = None
FEED_ATOM = None
FEED_DOMAIN = None
FEED_RSS = None

GOOGLE_ANALYTICS = "UA-40703057-1"

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

LINKS = None

PDF_GENERATOR = True

PLUGINS = [
    'summary',
    'sitemap',
    'pelican_gist',
    'simple_footnotes',
    'i18n_subsites'
]
PLUGIN_PATHS = [
    '/home/smetj/data/projects/github/pelican-plugins'
]

PYGMENTS_STYLE = "manni"

# RELATIVE_URLS = True  # Uncomment following line if you want document-relative URLs when developing

SITENAME = u'Project site of Jelle Smet'
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
SITEURL = 'https://smetj.net'

STATIC_PATHS = [
    'pics',
    'robots.txt',
]

SOCIAL = (('twitter', 'http://twitter.com/smetj'),
          ('github', 'https://github.com/smetj'),)

SUMMARY_BEGIN_MARKER = "__start_summary__"
SUMMARY_END_MARKER = "__end_summary__"

TAG_FEED = None

THEME = '/home/smetj/data/projects/github/pelican-themes/pelican-bootstrap3'

TIMEZONE = 'Europe/Paris'

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
