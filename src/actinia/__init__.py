#!/usr/bin/env python

"""Initialize the actinia-python-client package.

actinia-python-client is a python client for actinia - an open source REST
API for scalable, distributed, high performance processing of geographical
data that uses GRASS GIS for computational tasks.

SPDX-FileCopyrightText: (c) 2022-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022-2025, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

from importlib.metadata import PackageNotFoundError, version

from actinia.actinia import Actinia as Actinia

try:
    # Change here if project is renamed and does not equal the package name
    __version__ = version(__name__).version
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
