#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Adil Sadik'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
SITENAME = "sparky005's house"
SITEURL = 'http://localhost:8000'
SITETITLE = AUTHOR
SITELOGO = 'https://secure.gravatar.com/avatar/d3a04321ec957b22cb686a882a63aff3?s=240'
FAVICON = 'https://secure.gravatar.com/avatar/d3a04321ec957b22cb686a882a63aff3?s=60'
PYGMENTS_STYLE = 'friendly'

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

MAIN_MENU = True
MENUITEMS = (('Categories', '/categories.html'),
             ('Archives', '/archives.html'),
             ('Tags', '/tags.html'))

HOME_HIDE_TAGS = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/sparky_005'),
          ('github', 'https://github.com/sparky005'),
          ('facebook', 'https://www.facebook.com/adilsadik'),
          ('linkedin', 'https://www.linkedin.com/in/adil-sadik-02ab6378/'),
          ('rss', 'feeds/all.atom.xml'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
#THEME = './themes/pelican-alchemy/alchemy'
#THEME = './themes/attila'
THEME='../../pelican-themes/medius'
PLUGIN_PATHS = ['../../pelican-plugins']
PLUGINS = ['render_math', 'post_stats']
STATIC_PATHS = ['images', 'extra/CNAME', 'downloads']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    }
