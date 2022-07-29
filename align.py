#!/usr/bin/env python

# taken from https://github.com/andrewphorn/markdown.textalign

'''
Text Alignment Extension for Python-Markdown
============================================

Allows markdown to center and right-align text.

Usage
-----

    >>> import markdown
    >>> text = """->This text is centered<- ->and this text is right-aligned->"""
    >>> html = markdown.markdown(text,["textalign"])
    >>> print(html)
    <p>
    <div style="display:block;text-align:center;">This text is centered</div>
    <div style="display:block;text-align:right;">and this text is right-aligned</div>
    </p>

Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)
'''


import markdown
from markdown.inlinepatterns import Pattern
from markdown.util import etree


CENTR_RE = r"(\-\>)(.+?)(\<\-)"
RIGHT_RE = r"(\-\>)(.+?)(\-\>)"


class CenterAlignPattern(Pattern):
    def handleMatch(self, m):
        txt = etree.Element("div")
        txt.set("style", "display:block;text-align:center;")
        txt.text = m.group(3)
        return txt


class RightAlignPattern(Pattern):
    def handleMatch(self, m):
        txt = etree.Element("div")
        txt.set("style", "display:block;text-align:right;")
        txt.text = m.group(3)
        return txt


class TextAlignExtension(markdown.extensions.Extension):
    """Adds textalign extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """Modifies inline patterns."""
        md.inlinePatterns.add("center", CenterAlignPattern(CENTR_RE), "<not_strong")
        md.inlinePatterns.add("right", RightAlignPattern(RIGHT_RE), "<not_strong")


def makeExtension(configs={}):
    return TextAlignExtension(configs=dict(configs))
