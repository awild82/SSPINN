# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "SSPINN: A utility to predict chemical structures from NMR data"
# Long description will go up on the pypi page
long_description = """

SSPINN (Spectral Structure Prediction In Neural Networks)
========
SSPINN is a neural net framework for predicting chemical structures from an
empirical formula and NMR (and possibly other) spectral data.

It comes with a set of pre-trained parameters that can be used to immediately
predict the structure of the chemical in the NMR spectrum.

Alternatively, it has the nmrshiftdb2 1H spectral database and is built on
keras, so a custom network design can be implemented and trained within this
package.

TODO: Insert citations

License
=======
``sspinn`` is licensed under the terms of the MIT license. See the file
"LICENSE" for information on the history of this software, terms & conditions
for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2018--, Lauren Koulias, Ian Murphy, Torin Stetina, Andrew Wildman
The University of Washington
"""

NAME = "sspinn"
MAINTAINER = "Andrew Wildman"
MAINTAINER_EMAIL = "apw4@uw.edu"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/awild82/SSPINN"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Lauren Koulias, Ian Murphy, Torin Stetina, Andrew Wildman"
AUTHOR_EMAIL = "koulil@uw.edu, imurphy@uw.esu, torins@uw.edu, apw4@uw.edu"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ["sspinn"]
PACKAGE_DATA = {'nets': ['sspinn/nets/hyak_long.h5']}
REQUIRES = []
