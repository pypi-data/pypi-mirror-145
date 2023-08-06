# pylint: disable=W0622
"""cubicweb-compound application packaging information"""

distname = 'cubicweb-compound'
modname = 'cubicweb_coumpound'

numversion = (0, 8, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Library cube to handle assemblies of composite entities'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {
    'cubicweb': ">= 3.26.19, < 3.36.0",
}

__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
