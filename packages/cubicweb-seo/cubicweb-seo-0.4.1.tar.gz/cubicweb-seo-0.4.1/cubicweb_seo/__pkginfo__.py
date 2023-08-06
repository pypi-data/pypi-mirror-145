# pylint: disable=W0622
"""cubicweb-seo application packaging information"""

modname = "cubicweb_seo"
distname = "cubicweb-seo"

numversion = (0, 4, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "search engine optimisation with robotstxt and sitemaps"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

__depends__ = {"cubicweb": ">= 3.27.0, < 3.35.0"}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
