# pylint: disable=W0622
"""cubicweb-wireit application packaging information"""

modname = 'wireit'
distname = 'cubicweb-wireit'

numversion = (1, 1, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'WireIt workflow store for the CubicWeb framework'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {'cubicweb': ">= 3.25.0, < 3.36.0",
               'cubicweb-file': None}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: JavaScript',
    ]
