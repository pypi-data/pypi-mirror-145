# pylint: disable=W0622
"""cubicweb-pwd-policy application packaging information"""


modname = 'cubicweb_pwd_policy'
distname = 'cubicweb-pwd-policy'

numversion = (1, 2, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Password policy for cubicweb applications'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {'cubicweb': ">= 3.24.7, < 3.36.0", 'six': '>= 1.4.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
