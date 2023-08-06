# -*- coding: utf-8 -*-
# pylint: disable=W0622
"""cubicweb-i18nfield application packaging information"""

modname = 'i18nfield'
distname = 'cubicweb-i18nfield'

numversion = (0, 3, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'Florent Cayré (Villejuif, FRANCE)'
author_email = 'Florent Cayré <florent.cayre@gmail.com>'
description = 'Provides a way to translate entity fields individually.'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': ">= 3.28, < 3.36.0",
    'cubicweb-card': '>= 0.5',
}

__recommends__ = {}
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: JavaScript',
]
