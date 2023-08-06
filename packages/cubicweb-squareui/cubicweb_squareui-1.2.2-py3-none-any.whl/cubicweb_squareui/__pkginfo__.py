# pylint: disable=W0622
"""cubicweb-squareui application packaging information"""

modname = 'squareui'
distname = 'cubicweb-squareui'

numversion = (1, 2, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'data-centric user interface for cubicweb based on bootstrap'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {
    'cubicweb': ">= 3.24.0, < 3.34.0",
    'cubicweb-bootstrap': '>= 1.3.1',
}

__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
