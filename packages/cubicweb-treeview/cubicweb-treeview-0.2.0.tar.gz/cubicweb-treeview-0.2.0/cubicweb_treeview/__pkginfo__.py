# pylint: disable=W0622
"""cubicweb-treeview application packaging information"""

modname = 'treeview'
distname = 'cubicweb-treeview'

numversion = (0, 2, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'tree-building adapters, widgets, views'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {'cubicweb': ">= 3.24.0, < 3.36.0"}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
