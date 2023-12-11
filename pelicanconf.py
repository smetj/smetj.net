AUTHOR = "Jelle Smet"

SITENAME = "Jelle Smet"
SITEURL = "https://smetj.net"

PATH = "content"

TIMEZONE = "Europe/Brussels"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = "feeds/blog-atom.xml"
FEED_ALL_RSS = "feeds/blog-rss.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_RSS = "feeds/{slug}-rss.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}-atom.xml"

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget

DEFAULT_PAGINATION = 20

import logging

LOG_FILTER = [(logging.WARN, "Empty alt attribute for image %s in %s")]


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

THEME = "theme/solarized"

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "admonition": {},
        "align:TextAlignExtension": {},
    },
    "output_format": "html5",
}


INDEX_SAVE_AS = "index.html"

MENUITEMS = [
    ("Home", ""),
    ("About", "about.html"),
    ("Feeds", "feeds.html"),
]
DISPLAY_CATEGORIES_ON_MENU = False

PLUGINS = ["pelican_gist", "simple_footnotes"]

GIST_PYGMENTS_STYLE = "solarized-light"
GIST_CACHE_ENABLED = False
