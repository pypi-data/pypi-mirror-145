# pylint: disable=W0622
"""cubicweb-dataprocessing application packaging information"""


modname = "dataprocessing"
distname = "cubicweb-dataprocessing"

numversion = (0, 5, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Data validation and transformation process"
web = "http://www.cubicweb.org/project/%s" % distname

__depends__ = {
    "cubicweb": ">= 3.24.0., < 3.36.0",
    "cubicweb-file": None,
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: JavaScript",
]
