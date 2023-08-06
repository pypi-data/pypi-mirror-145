# pylint: disable=W0622
"""cubicweb-elasticsearch application packaging information"""

modname = "elasticsearch"
distname = "cubicweb-elasticsearch"

numversion = (0, 11, 3)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Simple ElasticSearch indexing integration for CubicWeb"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

__depends__ = {
    "cubicweb": ">= 3.28.0, < 3.37.0",
    "six": ">= 1.4.0",
    "cwtags": None,
    "elasticsearch": ">=7.0.0,<8.0.0",
    "elasticsearch-dsl": ">=7.0.0,<8.0.0",
    "beautifulsoup4": None,
}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
